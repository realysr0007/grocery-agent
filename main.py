from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from agents.parser_agent import parse_grocery_message
from agents.price_checker import check_prices
from agents.payment_agent import create_payment_link
import os

load_dotenv()

app = FastAPI()

user_sessions = {}

@app.get("/")
async def root():
    return {"message": "Grocery Agent is running!"}

@app.post("/whatsapp")
async def whatsapp_reply(request: Request):
    form_data = await request.form()
    incoming_message = form_data.get("Body", "").strip()
    phone_number = form_data.get("From", "")
    print(f"Message from: {phone_number}")
    print(f"Message content: '{incoming_message}'")
    print(f"Has alnum: {any(c.isalnum() for c in incoming_message)}")

    response = MessagingResponse()

    # empty message handling
    if not incoming_message or not any(c.isalnum() for c in incoming_message):
        response.message("👋 Hi! Send me a grocery list and I'll find the best prices for you!\n\nExample: 2 litre milk, dozen eggs, brown bread")
    return Response(content=str(response), media_type="application/xml")
    
    # print(f"Raw message: '{incoming_message}'")
    # print(f"Length: {len(incoming_message)}")
    # print(f"Is empty: {not incoming_message}")

    if phone_number in user_sessions and user_sessions[phone_number]["state"] == "waiting_for_confirmation":
        if incoming_message.upper() == "YES":
            session = user_sessions[phone_number]
            try:
                payment_link = create_payment_link(
                    session['total'],
                    session['platform'],
                    session['parsed_response']
                )
                reply = f"✅ Order Confirmed!\n\nPlatform: {session['platform']}\nTotal: ₹{session['total']}\n\n💳 Complete your payment:\n{payment_link}\n\nOrder will be placed after payment! 🛒"
            except Exception as e:
                print(f"Payment link error: {e}")
                reply = "😕 Sorry, payment link generation failed. Please try again!"
            del user_sessions[phone_number]
        elif incoming_message.upper() == "NO":
            reply = "❌ Order cancelled. Send me a new grocery list anytime!"
            del user_sessions[phone_number]
        else:
            reply = "Please reply YES to confirm or NO to cancel."
    else:
        parsed_response = parse_grocery_message(incoming_message)
        print(f"Parsed: {parsed_response}")
        price_comparison = check_prices(parsed_response)
        print(f"Price comparison: {price_comparison}")
        platform = "Instamart" if "Instamart saves" in price_comparison else "Blinkit"
        total = ""
        for line in price_comparison.split("\n"):
            if platform + ":" in line:
                total = line.split("₹")[-1].strip()
            print(f"Extracted total: '{total}'")
            print(f"Platform: '{platform}'")
            print(f"Price comparison: {price_comparison}")
        if not total or total == "0":
            reply = "😕 Sorry, I couldn't find any of those items in our database.\n\nAvailable items: milk, eggs, bread, butter, rice, sugar, salt, oil, onion, tomato\n\nPlease try again with items from the list!"
        else:
            user_sessions[phone_number] = {
                "state": "waiting_for_confirmation",
                "parsed_response": parsed_response,
                "platform": platform,
                "total": total
            }
            print(f"Session saved for {phone_number}: {user_sessions[phone_number]}")
            reply = price_comparison

    response.message(reply)
    return Response(content=str(response), media_type="application/xml")
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

    response = MessagingResponse()

    if phone_number in user_sessions and user_sessions[phone_number]["state"] == "waiting_for_confirmation":
        if incoming_message.upper() == "YES":
            session = user_sessions[phone_number]
            payment_link = create_payment_link(
                session['total'],
                session['platform'],
                session['parsed_response']
            )
            reply = f"✅ Order Confirmed!\n\nPlatform: {session['platform']}\nTotal: ₹{session['total']}\n\n💳 Complete your payment:\n{payment_link}\n\nOrder will be placed after payment! 🛒"
            del user_sessions[phone_number]
        elif incoming_message.upper() == "NO":
            reply = "❌ Order cancelled. Send me a new grocery list anytime!"
            del user_sessions[phone_number]
        else:
            reply = "Please reply YES to confirm or NO to cancel."
    else:
        parsed_response = parse_grocery_message(incoming_message)
        price_comparison = check_prices(parsed_response)
        platform = "Instamart" if "Instamart saves" in price_comparison else "Blinkit"
        total = ""
        for line in price_comparison.split("\n"):
            if platform + ":" in line:
                total = line.split("₹")[-1].strip()
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
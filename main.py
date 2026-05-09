from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from agents.parser_agent import parse_grocery_message
from agents.price_checker import check_prices
import os

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Grocery Agent is running!"}

@app.post("/whatsapp")
async def whatsapp_reply(request: Request):
    form_data = await request.form()
    incoming_message = form_data.get("Body", "")
    
    # Step 1 - parse the raw WhatsApp message
    parsed_response = parse_grocery_message(incoming_message)

    # Step 2 - check prices on parsed result
    price_comparison = check_prices(parsed_response)

    # Step 3 - send price comparison back to WhatsApp
    response = MessagingResponse()
    response.message(price_comparison)

    from fastapi.responses import Response
    return Response(content=str(response), media_type="application/xml")
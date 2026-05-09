from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from agents.parser_agent import parse_grocery_message
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
    
    parsed_response = parse_grocery_message(incoming_message)

    response = MessagingResponse()
    response.message(parsed_response)

    from fastapi.responses import Response
    return Response(content=str(response), media_type="application/xml")
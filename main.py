from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
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
    response = MessagingResponse()
    response.message(f"You said testing the changes: {incoming_message}")  
    from fastapi.responses import Response
    return Response(content=str(response), media_type="application/xml")
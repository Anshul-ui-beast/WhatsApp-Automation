from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(account_sid, auth_token)

def send_whatsapp_message(to: str, body: str):
    """
    Send a WhatsApp message via Twilio sandbox.
    """
    message = client.messages.create(
        from_=from_number,
        to=to,
        body=body,
    )
    return message.sid
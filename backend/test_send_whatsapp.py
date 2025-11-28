from whatsapp_client import send_whatsapp_message
import os
from dotenv import load_dotenv

load_dotenv()

to = os.getenv("TEST_WHATSAPP_NUMBER")

sid = send_whatsapp_message(to, "Test: EggsInvest WhatsApp integration is working ✅")
print("Sent message SID:", sid)
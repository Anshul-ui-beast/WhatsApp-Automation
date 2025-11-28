# from fastapi import FastAPI, Request
# from twilio.twiml.messaging_response import MessagingResponse

# app = FastAPI()

# @app.get("/")
# def root():
#     return {"status": "ok"}

# @app.post("/whatsapp/webhook")
# async def whatsapp_webhook(request: Request):
#     data = await request.form()
#     print("Incoming WhatsApp data:", dict(data))

#     # Auto reply
#     response = MessagingResponse()
#     response.message("Thanks for your message! The system received it successfully.")

#     return str(response)


# from fastapi import FastAPI, Request
# from backend.whatsapp_client import send_whatsapp_message
# from backend.whatsapp_templates import agent_intro_message
# from backend.db_client import log_message
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = FastAPI()

# @app.get("/")
# def root():
#     return {"status": "ok", "message": "EggsInvest backend running"}

# @app.post("/send-test-intro")
# def send_test_intro():
#     """
#     Simple endpoint to send an intro message to your own WhatsApp number.
#     Later this will send to agents from DB/CSV.
#     """
#     to = os.getenv("TEST_WHATSAPP_NUMBER")
#     body = agent_intro_message()
#     sid = send_whatsapp_message(to, body)

#     # log in DB
#     log_message(
#         direction="outbound",
#         whatsapp_number=to,
#         role="agent",
#         text=body,
#         status="sent",
#         provider_id=sid,
#     )

#     return {"sent_to": to, "sid": sid, "body": body}


from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from backend.whatsapp_client import send_whatsapp_message
from backend.whatsapp_templates import agent_intro_message
from backend.db_client import log_message
from backend.send_bulk_messages import send_intro_to_all_agents
from backend.classifier import classify_reply
from backend.db_client import update_agent_status

from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

# Initialize FastAPI App
app = FastAPI()


# ---------------------------
# 1. Root endpoint
# ---------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "EggsInvest backend running"}


# ---------------------------
# 2. Send test intro message
# ---------------------------
@app.post("/send-test-intro")
def send_test_intro():
    to = os.getenv("TEST_WHATSAPP_NUMBER")
    body = agent_intro_message()
    sid = send_whatsapp_message(to, body)

    # Log outbound message
    log_message(
        direction="outbound",
        whatsapp_number=to,
        role="agent",
        text=body,
        status="sent",
        provider_id=sid,
        template_name="intro"
    )

    return {"sent_to": to, "sid": sid, "body": body}


# ---------------------------
# 3. Webhook (NEW PART)
# ---------------------------
# @app.post("/whatsapp-webhook")
# async def whatsapp_webhook(request: Request):
#     try:
#         # Twilio sends x-www-form-urlencoded, but sometimes empty or json (status callbacks)
#         try:
#             form = await request.form()
#         except:
#             form = {}

#         from_number = form.get("From")
#         body = form.get("Body")
#         msg_sid = form.get("MessageSid")

#         print("Webhook received:", form)

#         # If Twilio sent a ping / empty request, avoid crashing
#         if not from_number:
#             return {"status": "ignored", "reason": "no sender"}

#         # Log inbound message
#         log_message(
#             direction="inbound",
#             whatsapp_number=from_number,
#             role="agent",
#             template_name=None,
#             text=body,
#             status="received",
#             provider_id=msg_sid
#         )

#         # Auto-response
#         from backend.whatsapp_client import send_whatsapp_message
#         auto_reply = (
#             "Thanks for your message! Our system has received your response. "
#             "We’ll get back to you shortly."
#         )
#         send_whatsapp_message(from_number, auto_reply)

#         return {"status": "ok"}

#     except Exception as e:
#         print("WEBHOOK ERROR:", e)
#         return {"status": "error", "detail": str(e)}


# @app.post("/whatsapp-webhook")
# async def whatsapp_webhook(request: Request):
#     raw = await request.body()
#     data = urllib.parse.parse_qs(raw.decode())

#     print("RAW:", raw)
#     print("PARSED:", data)

#     from_number = data.get("From", [""])[0]
#     body = data.get("Body", [""])[0]
#     msg_sid = data.get("MessageSid", [""])[0]

#     print("Incoming message:", from_number, body)

#     # Log inbound
#     log_message(
#         direction="inbound",
#         whatsapp_number=from_number,
#         role="agent",
#         text=body,
#         status="received",
#         provider_id=msg_sid
#     )

#     # Auto reply
#     send_whatsapp_message(from_number, "Thanks! Received ✅")

#     return "OK"

@app.post("/whatsapp-webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()   # ✅ Correct for Twilio

    from_number = form.get("From")
    body = form.get("Body")
    msg_sid = form.get("MessageSid")

    print("Incoming WhatsApp message:", from_number, body)

    # classify message
    classification = classify_reply(body)

    # Log inbound
    log_message(
        direction="inbound",
        whatsapp_number=from_number,
        role="agent",
        template_name=None,
        text=body,
        status="received",
        provider_id=msg_sid
    )

    # Update CRM
    update_agent_status(from_number, classification)

    # Auto-response
    from backend.whatsapp_client import send_whatsapp_message

    if classification == "interested":
        send_whatsapp_message(from_number,
            "Amazing — we'll send selected investment opportunities soon ✅")

    elif classification == "not_interested":
        send_whatsapp_message(from_number,
            "Totally fine — thanks for responding! 👍")

    elif classification == "follow_up":
        send_whatsapp_message(from_number,
            "Sure — please tell us your investment budget?")

    else:
        send_whatsapp_message(from_number,
            "Thanks — just confirming, are you open to receiving property listings?")

    return {"status": "ok", "classification": classification}

@app.post("/send-intro-to-all")
def send_intro_to_all():
    results = send_intro_to_all_agents()
    return {"total_sent": len(results), "details": results}

    # Respond back to Twilio
    return PlainTextResponse("Message received")
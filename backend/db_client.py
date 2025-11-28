# import mysql.connector
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def get_db():
#     conn = mysql.connector.connect(
#         host=os.getenv("DB_HOST"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         database=os.getenv("DB_NAME"),
#     )
#     return conn

# def log_message(direction, whatsapp_number, role, text, status, provider_id=None):
#     conn = get_db()
#     cur = conn.cursor()
#     sql = """
#         INSERT INTO messages (direction, whatsapp_number, role, message_text, status, meta_message_id)
#         VALUES (%s, %s, %s, %s, %s, %s)
#     """
#     cur.execute(sql, (direction, whatsapp_number, role, text, status, provider_id))
#     conn.commit()
#     cur.close()
#     conn.close()



import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

def log_message(direction, whatsapp_number, role, text, status, provider_id=None, template_name=None):
    """
    Logs both inbound and outbound WhatsApp messages.
    Matches EXACT columns in your messages table:
    
    id (auto)
    direction
    whatsapp_number
    role
    template_name
    message_text
    status
    meta_message_id
    created_at (auto)
    """
    conn = get_db()
    cur = conn.cursor()

    sql = """
        INSERT INTO messages (
            direction,
            whatsapp_number,
            role,
            template_name,
            message_text,
            status,
            meta_message_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        direction,
        whatsapp_number,
        role,
        template_name,     # can be None
        text,
        status,
        provider_id        # Twilio message SID
    )

    cur.execute(sql, values)
    conn.commit()
    cur.close()
    conn.close()
    
def update_agent_status(phone, status):
    conn = get_db()
    cur = conn.cursor()

    sql = "UPDATE agents SET lead_status=%s WHERE phone_whatsapp=%s"
    cur.execute(sql, (status, phone))

    conn.commit()
    cur.close()
    conn.close()

# -------------------------
# BUYER DATABASE HELPERS
# -------------------------

def get_buyer_by_phone(whatsapp_number):
    """Return buyer row matching a WhatsApp number."""
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM buyers
        WHERE whatsapp_number = %s
        LIMIT 1
    """
    cur.execute(sql, (whatsapp_number,))
    buyer = cur.fetchone()

    cur.close()
    conn.close()
    return buyer


def update_buyer_notes(whatsapp_number, new_notes):
    """Append new notes to buyer profile."""
    conn = get_db()
    cur = conn.cursor()

    sql = """
        UPDATE buyers
        SET notes = CONCAT(COALESCE(notes, ''), %s, '\n')
        WHERE whatsapp_number = %s
    """

    cur.execute(sql, (new_notes, whatsapp_number))
    conn.commit()

    cur.close()
    conn.close()


def update_buyer_status(whatsapp_number, status):
    """Track qualification stage — e.g. interested, follow_up, not_interested."""
    conn = get_db()
    cur = conn.cursor()

    sql = """
        UPDATE buyers
        SET status = %s
        WHERE whatsapp_number = %s
    """

    cur.execute(sql, (status, whatsapp_number))
    conn.commit()

    cur.close()
    conn.close()

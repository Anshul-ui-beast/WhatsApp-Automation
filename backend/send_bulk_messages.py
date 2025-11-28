from backend.db_client import get_db, log_message
from backend.whatsapp_templates import agent_intro_message
from backend.whatsapp_client import send_whatsapp_message

def send_intro_to_all_agents():
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id, name, phone_whatsapp, agency_name FROM agents")
    agents = cur.fetchall()

    results = []

    for agent in agents:
        body = agent_intro_message(agent["name"])
        to = agent["phone_whatsapp"]

        sid = send_whatsapp_message(to, body)

        log_message(
            direction="outbound",
            whatsapp_number=to,
            role="agent",
            template_name="intro",
            text=body,
            status="sent",
            provider_id=sid
        )

        results.append({"agent": agent["name"], "to": to, "sid": sid})

    cur.close()
    conn.close()

    return results

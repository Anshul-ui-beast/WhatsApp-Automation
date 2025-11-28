def agent_intro_message(agent_name: str = None):
    base = (
        "Hi{agent_part}, this is EggsInvest. "
        "We help investors connect with UK estate agents and off-market deals. "
        "Are you open to sharing selected listings via WhatsApp for potential investors?"
    )
    if agent_name:
        agent_part = f" {agent_name}"
    else:
        agent_part = ""
    return base.format(agent_part=agent_part)
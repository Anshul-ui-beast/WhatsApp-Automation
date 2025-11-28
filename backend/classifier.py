def classify_reply(text: str) -> str:
    if not text:
        return "invalid"

    t = text.lower().strip()

    positive = ["yes", "yeah", "yep", "interested", "sure", "okay"]
    negative = ["no", "not interested", "stop", "unsubscribe"]
    followup = ["send info", "details", "more", "pricing"]

    if any(p in t for p in positive):
        return "interested"
    if any(n in t for n in negative):
        return "not_interested"
    if any(f in t for f in followup):
        return "follow_up"

    return "unknown"

def detect_intent(text):
    """
    Categorizes transcribed speech into presentation actions.
    Priority is given to navigation commands to prevent logic overlaps.
    """
    text = text.lower().strip()
    intent = {"action": "NONE"}

    # 1. Navigation: Backwards (Priority)
    prev_triggers = ["previous", "back", "return", "last", "earlier", "before"]
    if any(word in text for word in prev_triggers):
        intent["action"] = "PREVIOUS_SLIDE"
        return intent
    
    # 2. Navigation: Forwards
    next_triggers = ["next", "topic", "forward", "continue", "move", "advance"]
    if any(word in text for word in next_triggers):
        intent["action"] = "NEXT_SLIDE"
        return intent

    # 3. Features: Zoom/Detail
    zoom_triggers = ["example", "zoom", "look", "show", "illustration"]
    if any(word in text for word in zoom_triggers):
        intent["action"] = "ZOOM_IN"
        return intent

    return intent
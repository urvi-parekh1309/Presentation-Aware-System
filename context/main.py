from context.context_manager import ContextManager


def parse_input(user_input):
    """
    Converts simple text into intent format.
    Temporary simulation of speech module.
    """
    text = user_input.lower()
    words = text.split()

    # -------- NEXT SLIDE --------
    if any(phrase in text for phrase in [
        "next", "forward", "advance", "proceed",
        "continue", "move on", "moving on",
        "go ahead", "onwards", "moving ahead"
    ]):
        return {"intent": "next_slide", "confidence": 0.9}

    # -------- PREVIOUS SLIDE --------
    elif any(phrase in text for phrase in [
        "back", "previous", "prior", "last",
        "go back", "return", "rewind"
    ]):
        return {"intent": "previous_slide", "confidence": 0.9}

    # -------- UNDO --------
    elif "undo" in words:
        return {"intent": "undo", "confidence": 0.9}

    # -------- HIGHLIGHT --------
    elif "highlight" in words:
        target = words[-1] if len(words) > 1 else None
        return {"intent": "highlight", "target": target, "confidence": 0.9}

    # -------- JUMP TO SLIDE --------
    elif any(phrase in text for phrase in ["jump to", "go to", "slide"]):
        for word in words:
            if word.isdigit():
                return {"intent": "jump_to_slide", "target": word, "confidence": 0.9}

    # -------- ZOOM --------
    elif "zoom in" in text:
        return {"intent": "zoom_in", "confidence": 0.9}

    elif "zoom out" in text:
        return {"intent": "zoom_out", "confidence": 0.9}

    # -------- MUTE / UNMUTE --------
    elif "unmute" in words:
        return {"intent": "unmute", "confidence": 0.9}

    elif "mute" in words:
        return {"intent": "mute", "confidence": 0.9}

    # -------- CLEAR HIGHLIGHTS --------
    elif "clear" in words:
        return {"intent": "clear_highlights", "confidence": 0.9}

    # -------- SUMMARY --------
    elif "summary" in words:
        return {"intent": "show_summary", "confidence": 0.9}

    # -------- UNKNOWN --------
    return {"intent": "none", "confidence": 0.9}


def run_system():
    context = ContextManager()
    context.state.set_total_slides(5)

    print("=" * 40)
    print("  VOICE PRESENTATION ASSISTANT")
    print("=" * 40)
    print("Commands: next, back, highlight [word],")
    print("jump to [number], zoom in, zoom out,")
    print("mute, unmute, clear highlights, summary, undo, exit")
    print("=" * 40)

    while True:

        # -------- SHOW CURRENT STATE --------
        print(f"\n Slide {context.state.current_slide + 1} of {context.state.total_slides}")
        print(f" Last command: {context.state.last_intent}")
        print(f" Muted: {context.state.is_muted}")

        user_input = input("\nEnter command: ")

        # -------- EXIT --------
        if user_input.lower() == "exit":
            summary = context.state.get_session_summary()
            print("\n SESSION SUMMARY")
            print(f" Total commands : {summary['total_commands']}")
            print(f" Successful     : {summary['successful']}")
            print(f" Failed         : {summary['failed']}")
            print(f" Highlights made: {summary['highlights_made']}")
            context.history.export_log()
            break

        # -------- PARSE & PROCESS --------
        intent_data = parse_input(user_input)

        print(f" Confidence: {intent_data['confidence']}")

        result = context.process_intent(intent_data)

        context.state.log_command(
            intent_data["intent"],
            success=result.get("status") != "error"
        )

        print("Output:", result)
        print("-" * 40)


if __name__ == "__main__":
    run_system()
class IntentValidator:

    VALID_INTENTS = {
        "next_slide",
        "previous_slide",
        "highlight",
        "undo",
        "none",
        "jump_to_slide",
        "zoom_in",
        "zoom_out",
        "laser_pointer",
        "mute",
        "unmute",
        "start_timer",
        "stop_timer",
        "show_summary",
        "clear_highlights",
    }

    MIN_CONFIDENCE = 0.5
    LOW_CONFIDENCE_THRESHOLD = 0.65

    def validate(self, intent_data):

        # -------- BASIC INPUT CHECK --------
        if not isinstance(intent_data, dict):
            return False, "Invalid input format"

        intent = intent_data.get("intent")
        confidence = intent_data.get("confidence", 1.0)

        # -------- INTENT CHECK --------
        if not intent:
            return False, "No intent provided"

        if intent not in self.VALID_INTENTS:
            return False, f"Invalid intent: {intent}"

        # -------- CONFIDENCE CHECK --------
        if not isinstance(confidence, (int, float)):
            return False, "Invalid confidence value"

        if confidence < self.MIN_CONFIDENCE:
            return False, "Low confidence"

        # -------- TARGET CHECK --------
        if intent == "highlight":
            target = intent_data.get("target")
            if not target:
                return False, "Missing target for highlight"

        if intent == "jump_to_slide":
            target = intent_data.get("target")
            if not target or not str(target).isdigit():
                return False, "Missing or invalid slide number for jump_to_slide"

        # -------- LOW CONFIDENCE FLAG --------
        if confidence < self.LOW_CONFIDENCE_THRESHOLD:
            return True, "low_confidence"

        return True, "valid"
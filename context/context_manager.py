from context.state import SystemState
from context.history_manager import HistoryManager
from context.intent_validator import IntentValidator


class ContextManager:
    """Processes validated intents and manages presentation state."""

    def __init__(self):
        self.state = SystemState()
        self.history = HistoryManager()
        self.validator = IntentValidator()

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def process_intent(self, intent_data: dict) -> dict:
        valid, message = self.validator.validate(intent_data)

        if not valid:
            self.state.log_command(intent_data.get("intent"), success=False)
            return self._error(message)

        # Did you mean? trigger for low confidence
        if message == "low_confidence":
            print(f"Low confidence detected. Did you mean: '{intent_data['intent']}'?")
            return {
                "status": "low_confidence",
                "suggestion": intent_data["intent"],
                "message": "Please confirm your command"
            }

        intent = intent_data["intent"]
        target = intent_data.get("target")

        if target == "this":
            target = self.state.last_target

        handler = self._get_handler(intent)
        if handler is None:
            return self._error(f"Unknown intent: {intent!r}")

        result = handler(target)

        if result.get("status") != "error":
            self.state.set_last_action(intent, target)
            self.history.add_action(intent, target)
            self.state.log_command(intent, success=True)

        return result

    # ------------------------------------------------------------------ #
    # Intent Handlers                                                      #
    # ------------------------------------------------------------------ #

    def _handle_next_slide(self, _target) -> dict:
        if self.state.current_slide >= self.state.total_slides - 1:
            return self._error("Already at last slide")
        self.state.update_slide(self.state.current_slide + 1)
        return {"action": "next_slide", "current_slide": self.state.current_slide}

    def _handle_previous_slide(self, _target) -> dict:
        if self.state.current_slide > 0:
            self.state.update_slide(self.state.current_slide - 1)
        return {"action": "previous_slide", "current_slide": self.state.current_slide}

    def _handle_highlight(self, target) -> dict:
        self.state.add_highlight(self.state.current_slide, target)
        return {
            "action": "highlight",
            "target": target,
            "current_slide": self.state.current_slide
        }

    def _handle_undo(self, _target) -> dict:
        last_action = self.history.undo()
        if last_action is None:
            return self._error("Nothing to undo")
        self._reverse_action(last_action)
        return {
            "action": "undo",
            "reversed_action": last_action,
            "current_slide": self.state.current_slide,
        }

    def _handle_jump_to_slide(self, target) -> dict:
        if target and str(target).isdigit():
            self.state.update_slide(int(target) - 1)
            return {"action": "jump_to_slide", "current_slide": self.state.current_slide}
        return self._error("Invalid slide number")

    def _handle_zoom_in(self, _target) -> dict:
        return {"action": "zoom_in", "slide": self.state.current_slide}

    def _handle_zoom_out(self, _target) -> dict:
        return {"action": "zoom_out", "slide": self.state.current_slide}

    def _handle_mute(self, _target) -> dict:
        self.state.is_muted = True
        return {"action": "muted"}

    def _handle_unmute(self, _target) -> dict:
        self.state.is_muted = False
        return {"action": "unmuted"}

    def _handle_clear_highlights(self, _target) -> dict:
        self.state.highlights.clear()
        return {"action": "highlights_cleared"}

    def _handle_show_summary(self, _target) -> dict:
        summary = self.state.get_session_summary()
        print("Session Summary:", summary)
        return {"action": "show_summary", "summary": summary}

    # ------------------------------------------------------------------ #
    # History Utilities                                                    #
    # ------------------------------------------------------------------ #

    def get_last_n(self, n=10) -> list:
        return self.history.get_last_n(n)

    def export_log(self, filename="session_log.txt") -> None:
        self.history.export_log(filename)

    def get_command_count(self) -> int:
        return self.history.get_command_count()

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    def _get_handler(self, intent: str):
        return {
            "next_slide":       self._handle_next_slide,
            "previous_slide":   self._handle_previous_slide,
            "highlight":        self._handle_highlight,
            "undo":             self._handle_undo,
            "jump_to_slide":    self._handle_jump_to_slide,
            "zoom_in":          self._handle_zoom_in,
            "zoom_out":         self._handle_zoom_out,
            "mute":             self._handle_mute,
            "unmute":           self._handle_unmute,
            "clear_highlights": self._handle_clear_highlights,
            "show_summary":     self._handle_show_summary,
        }.get(intent)

    def _reverse_action(self, action: dict) -> None:
        match action["intent"]:
            case "next_slide":
                self.state.update_slide(max(0, self.state.current_slide - 1))
            case "previous_slide":
                self.state.update_slide(self.state.current_slide + 1)
            case "highlight":
                self.state.remove_last_highlight()

    @staticmethod
    def _error(message: str) -> dict:
        return {"status": "error", "message": message}
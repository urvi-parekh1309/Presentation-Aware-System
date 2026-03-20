class SystemState:

    def __init__(self):
        self.current_slide = 0
        self.total_slides = 0
        self.last_intent = None
        self.last_target = None
        self.confidence = 1.0
        self.command_history_log = []
        self.successful_commands = 0
        self.failed_commands = 0
        self.highlights = []
        self.is_muted = False

    # ------------------------------------------------------------------ #
    # Slide Management                                                     #
    # ------------------------------------------------------------------ #

    def update_slide(self, slide_number):
        if not isinstance(slide_number, int):
            return
        if slide_number < 0:
            self.current_slide = 0
        elif self.total_slides and slide_number >= self.total_slides:
            self.current_slide = self.total_slides - 1
        else:
            self.current_slide = slide_number

    def set_total_slides(self, total):
        if isinstance(total, int) and total >= 0:
            self.total_slides = total

    # ------------------------------------------------------------------ #
    # Action Tracking                                                      #
    # ------------------------------------------------------------------ #

    def set_last_action(self, intent, target=None, confidence=1.0):
        self.last_intent = intent
        self.last_target = target
        self.confidence = confidence

    def log_command(self, intent, success=True):
        self.command_history_log.append({
            "intent": intent,
            "success": success
        })
        if success:
            self.successful_commands += 1
        else:
            self.failed_commands += 1

    # ------------------------------------------------------------------ #
    # Highlight Management                                                 #
    # ------------------------------------------------------------------ #

    def add_highlight(self, slide_number, target):
        self.highlights.append({
            "slide": slide_number,
            "target": target
        })

    def get_highlights_for_slide(self, slide_number):
        return [h for h in self.highlights if h["slide"] == slide_number]

    def remove_last_highlight(self):
        if self.highlights:
            return self.highlights.pop()
        return None

    # ------------------------------------------------------------------ #
    # State Access                                                         #
    # ------------------------------------------------------------------ #

    def get_state(self):
        return {
            "current_slide": self.current_slide,
            "total_slides": self.total_slides,
            "last_intent": self.last_intent,
            "last_target": self.last_target,
            "confidence": self.confidence,
            "is_muted": self.is_muted,
            "highlights": self.highlights
        }

    def get_session_summary(self):
        return {
            "total_commands": len(self.command_history_log),
            "successful": self.successful_commands,
            "failed": self.failed_commands,
            "highlights_made": len(self.highlights)
        }

    # ------------------------------------------------------------------ #
    # Utilities                                                            #
    # ------------------------------------------------------------------ #

    def reset(self):
        self.current_slide = 0
        self.last_intent = None
        self.last_target = None
        self.confidence = 1.0
        self.command_history_log = []
        self.successful_commands = 0
        self.failed_commands = 0
        self.highlights = []
        self.is_muted = False
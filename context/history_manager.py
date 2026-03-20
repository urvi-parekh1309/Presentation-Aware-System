class HistoryManager:

    def __init__(self, max_size=50):
        self.history = []
        self.max_size = max_size

    # ------------------------------------------------------------------ #
    # Core Actions                                                         #
    # ------------------------------------------------------------------ #

    def add_action(self, intent, target=None):
        action = {
            "intent": intent,
            "target": target
        }

        # Maintain max history size
        if len(self.history) >= self.max_size:
            self.history.pop(0)

        self.history.append(action)

    def undo(self):
        if self.history:
            return self.history.pop()
        return None

    def peek_last(self):
        if self.history:
            return self.history[-1]
        return None

    def clear(self):
        self.history.clear()

    # ------------------------------------------------------------------ #
    # History Utilities                                                    #
    # ------------------------------------------------------------------ #

    def show_history(self):
        return list(self.history)

    def get_last_n(self, n=10):
        if len(self.history) >= n:
            return self.history[-n:]
        return self.history

    def get_command_count(self):
        return len(self.history)

    # ------------------------------------------------------------------ #
    # Log Export                                                           #
    # ------------------------------------------------------------------ #

    def export_log(self, filename="session_log.txt"):
        with open(filename, "w") as f:
            for i, action in enumerate(self.history):
                f.write(f"{i+1}. Intent: {action['intent']} | Target: {action['target']}\n")
        print(f"Log saved to {filename}")
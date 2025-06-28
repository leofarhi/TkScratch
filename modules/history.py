MAX_UNDO_HISTORY = 15

class HistoryManager:
    def __init__(self, push_callback=None, apply_callback=None):
        self.history = []
        self.redo_stack = []
        self.push_callback = push_callback
        self.apply_callback = apply_callback

    def push(self):
        if not self.push_callback or not self.apply_callback:
            raise ValueError("Callbacks must be set before using HistoryManager")
        snapshot = self.push_callback()
        self.history.append(snapshot)
        self.redo_stack.clear()
        if len(self.history) > MAX_UNDO_HISTORY:
            self.history.pop(0)

    def undo(self):
        if not self.apply_callback:
            raise ValueError("Apply callback must be set")
        if self.history:
            current_state = self.push_callback()
            snapshot = self.history.pop()
            self.redo_stack.append(current_state)
            self.apply_callback(snapshot)

    def get_last_action(self):
        if self.history:
            return self.history[-1]
        return None

    def redo(self):
        if not self.apply_callback:
            raise ValueError("Apply callback must be set")
        if self.redo_stack:
            current_state = self.push_callback()
            snapshot = self.redo_stack.pop()
            self.history.append(current_state)
            self.apply_callback(snapshot)

    def clear(self):
        self.history.clear()
        self.redo_stack.clear()

    def can_undo(self):
        return len(self.history) > 0
    def can_redo(self):
        return len(self.redo_stack) > 0

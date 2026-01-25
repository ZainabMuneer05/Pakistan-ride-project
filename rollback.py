class RollbackManager:
    def __init__(self, limit=10):
        self.stack = []
        self.limit = limit
    def push(self, data):
        if len(self.stack) >= self.limit: self.stack.pop(0)
        self.stack.append(data)
    def undo(self):
        return self.stack.pop() if self.stack else None
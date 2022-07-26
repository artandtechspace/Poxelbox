
class BaseUserInput:
    # Change handler for when the player-controlls change
    _on_change = None

    def start(self, on_change):
        self._on_change = on_change
        pass

    def update(self):
        pass

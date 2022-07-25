
class BaseUserInput:
    # Change handler for when the player-controlls change
    __on_change = None

    def start(self, on_change):
        self.__on_change = on_change
        pass

    def update(self):
        pass

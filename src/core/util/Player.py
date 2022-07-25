class Player:
    # Status-code of the player (Without the player obviously)
    __status: int

    __player_id: int

    __on_change: None

    def get_id(self):
        return self.__player_id

    def init(self, player_id: int, on_change):
        self.__status = player_id
        self.__player_id = player_id
        self.__on_change = on_change

    def update_status(self, status):
        # Gets the status differences
        diff = status ^ self.__status

        # Executes the event's for the changes
        for i in range(8):
            if ((diff >> i) & 1) == 1:
                self.__on_change(self, i, True if (status >> i) & 1 else False)

        # Updates the status
        self.__status = status

    # Returns if the given button is pressed. Use the button-constants from the Controller-File
    def is_pressed(self, key: int):
        return True if (self.__status >> key) & 1 else False

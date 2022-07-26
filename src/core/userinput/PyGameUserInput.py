import pygame
from core.userinput.BaseUserInput import BaseUserInput
import sys
from config.Config import PyGameUserInput_KEY_MAPPINGS_P1 as KEY_MAPPINGS_P1
from config.Config import PyGameUserInput_KEY_MAPPINGS_P2 as KEY_MAPPINGS_P2

class PyGameUserInput(BaseUserInput):
    p1_status = 0b000000000  # Keystatus and playerid of player 1
    p2_status = 0b000000001  # Keystatus and playerid of player 2

    def update(self):
        # Iterates over all events
        for event in pygame.event.get():

            # Checks for the window-close-event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Checks if the pressed key conforms to the mappings
            if event.type in [pygame.KEYUP, pygame.KEYDOWN] and (
                    event.key in KEY_MAPPINGS_P1 or event.key in KEY_MAPPINGS_P2):
                # Gets the bit-status (0 or 1)
                is_key_down = 1 if event.type == pygame.KEYDOWN else 0
                # Gets  the player (0 or 1)
                player = 0 if event.key in KEY_MAPPINGS_P1 else 1

                # Gets the mapped key (Appends plus one to filter out player-id)
                key_id = (KEY_MAPPINGS_P1[event.key] if player == 0 else KEY_MAPPINGS_P2[event.key]) + 1

                # Gets the current player status
                player_status = self.p1_status if player == 0 else self.p2_status

                # Checks if the state didn't change
                if player_status >> key_id & 1 == is_key_down:
                    continue

                # Calculates the new status
                new_status = player_status ^ (1 << key_id)

                # Updates the status
                if player == 0:
                    self.p1_status = new_status
                else:
                    self.p2_status = new_status

                # Pushes the update
                self._on_change(new_status)

from games.GameBase import GameBase
from core.util.Player import Player


class Snake(GameBase):

    def get_time_constant(self):
        return .1

    def on_player_input(self, player: Player, button: int, status: bool):
        pass
        # get executed when the player presses a button

    def update(self):
        pass
        # get executed every frame

from core.rendering.renderer.RendererBase import RendererBase
from core.util.Player import Player
from core.GameController import GameController


class GameBase:
    renderer: RendererBase
    player_one: Player
    player_two: Player
    game_controller: GameController

    def init(self, game_controller: GameController, renderer: RendererBase, player_one: Player, player_two: Player):
        self.renderer = renderer
        self.player_one = player_one
        self.player_two = player_two

    def get_time_constant(self):
        return .1

    # Called once every frame to update game logic
    def update(self):
        pass

    def on_player_input(self, player: Player, button: int, status: bool):
        pass

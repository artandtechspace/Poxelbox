from core.rendering.renderer.RendererBase import RendererBase
from core.util.Player import Player
from core.scenery.SceneController import SceneController


class SceneBase:
    # Renderer for the scene
    renderer: RendererBase

    # Players
    player_one: Player
    player_two: Player

    # Scene-controller
    scene_controller: SceneController

    def init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player, player_two: Player):
        self.renderer = renderer
        self.player_one = player_one
        self.player_two = player_two

    def get_time_constant(self):
        return .1

    # Called once every frame to update scene logic
    def update(self):
        pass

    def on_player_input(self, player: Player, button: int, status: bool):
        pass

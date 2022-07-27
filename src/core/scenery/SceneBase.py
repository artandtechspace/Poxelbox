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

    # Event: When starting the scene
    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player, player_two: Player):
        self.renderer = renderer
        self.player_one = player_one
        self.player_two = player_two

    # Used to get a time-constant that must be awaited until the next frame is updated
    # Given a larger number, the updates will come slower
    def get_time_constant(self):
        return .1

    # Event: Called once every frame to update the scene logic
    def on_update(self):
        pass

    # Event: Called when the state of any button from any player changes
    def on_player_input(self, player: Player, button: int, status: bool):
        pass

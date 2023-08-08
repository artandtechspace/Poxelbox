from core.scenery.SceneBase import SceneBase
from core.util.Player import Player
from config import ControllerKeys as Controller
from core.scenery.SceneController import SceneController
from core.rendering.renderer.RendererBase import RendererBase


class GameScene(SceneBase):

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)

    def get_time_constant(self):
        return super().get_time_constant()

    def on_update(self):
        super().on_update()

    # Checks if the input was the loading-screen and if so loads the loading screen as a scene
    # Returns true if the loading screen got loaded
    def on_handle_loading_screen(self, button: int, status: bool, set_scene = None):
        # Checks if select got pressed
        if button == Controller.BTN_SELECT and status:
            # Opens the loading screen scene
            from scenes.LoadingScreenScene import LoadingScreenScene
            self.scene_controller.load_scene(LoadingScreenScene(self if set_scene is None else set_scene))
            return True

        return False

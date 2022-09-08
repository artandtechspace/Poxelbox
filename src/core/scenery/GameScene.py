from core.scenery.SceneBase import SceneBase
from core.util.Player import Player
from config import ControllerKeys as Controller


class GameScene(SceneBase):
    def on_player_input(self, player: Player, button: int, status: bool):
        # Checks if select got pressed
        if button == Controller.BTN_SELECT and status:
            # Opens the loading screen scene
            from scenes.LoadingScreenScene import LoadingScreenScene
            self.scene_controller.load_scene(LoadingScreenScene())

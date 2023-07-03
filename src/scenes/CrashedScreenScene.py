from core.scenery.SceneBase import SceneBase
from core.scenery.SceneController import SceneController
from core.util.Player import Player
from core.rendering.renderer.RendererBase import RendererBase

# Colors to fill the screen with to indicate a crash
COLOR_ERROR_ONE = (133, 0, 0)
COLOR_ERROR_TWO = (176, 95, 0)

class CrashedScreenScene(SceneBase):

    def __init__(self):
        super().__init__()
        
        self.update_flag = False

    def get_time_constant(self):
        return 1.2

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)

    # Event: Called once every frame to update the scene logic
    def on_update(self):

        self.update_flag = not self.update_flag

        # Renders the error scene
        for x in range(self.renderer.screen.size_x):
            for y in range(self.renderer.screen.size_y):
                self.renderer.set_led(x, y, COLOR_ERROR_ONE if (y % 2 == x % 2) == self.update_flag else COLOR_ERROR_TWO)

        self.renderer.push_leds()

    def on_player_input(self, player: Player, button: int, status: bool):
        # Only acts on pull down
        if not status:
            return

        # Throws to player back to the selection screen
        from scenes.LoadingScreenScene import LoadingScreenScene
        self.scene_controller.load_scene(LoadingScreenScene())

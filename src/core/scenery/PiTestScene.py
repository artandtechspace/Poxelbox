from config import Colors
from core.scenery.SceneBase import SceneBase
from core.util.Player import Player
from core.util.Vector2D import Vector2D
from core.scenery.SceneController import SceneController
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerKeys as Controller
import config.Config as Cfg

COLORS_TO_TEST = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]


class PiTestScene(SceneBase):
    # Last updated position
    __pos = 0

    # Index of the color to use
    __clr_idx = 0

    def get_time_constant(self):
        return 0

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)

    def on_update(self):
        # Calculates the position on the screen based on the current position-id
        x = self.__pos % self.renderer.screen.size_x
        y = int(self.__pos / self.renderer.screen.size_x)

        # Checks if the id is outside the screen resolution
        if y >= self.renderer.screen.size_y:
            # Reset
            self.__pos = 0

            # Updates to the next color
            self.__clr_idx += 1

            # Resets to the first color if the last color got displayed
            if self.__clr_idx >= len(COLORS_TO_TEST):
                self.__clr_idx = 0
            return

        # Advances the position
        self.__pos += 1

        # Colors the pixel
        self.renderer.set_led(x, y, COLORS_TO_TEST[self.__clr_idx])
        self.renderer.push_leds()
        pass

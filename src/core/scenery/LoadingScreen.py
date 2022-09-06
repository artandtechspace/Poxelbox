from config import Colors
from core.scenery.SceneBase import SceneBase
from core.scenery.SceneController import SceneController
from core.util.Player import Player
from core.rendering.renderer.RendererBase import RendererBase
from PIL import Image
import config.Config as Cfg
from config import ControllerKeys as Controller
from games.snake import SnakeScene
import games.pong.PongScene as PongScene
from core.util.Vector2D import Vector2D

PREVIEWS = ["rsc//previews//pong.png"]


class LoadingScreen(SceneBase):
    images: []
    game_idx: int

    def get_time_constant(self):
        return .1

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        # Initialises variables
        super().on_init(scene_controller, renderer, player_one, player_two)
        self.scene_controller = scene_controller
        self.images = []

        # Loads every image
        for i in range(len(PREVIEWS)):
            self.images.append(Image.open(PREVIEWS[i]))
            # Raises Exception when the Image does not match the screen size
            if self.images[i].size != (renderer.screen.size_x, renderer.screen.size_y):
                raise Exception("Wrong Image size!")

        # loads the image and sets the game index to start value
        self.reload()

    def __display_image(self, idx: int):
        t_img = self.images[idx]
        # iterates through every pixel and displays the pixels colour at its position
        for x in range(t_img.size[0]):
            for y in range(t_img.size[1]):
                color = t_img.getpixel((x, y))[0:3]
                self.renderer.set_led(x, t_img.size[1] - y - 1, color)
        self.renderer.push_leds()

    # no updates needed
    def on_update(self):
        pass

    def on_player_input(self, player: Player, button: int, status: bool):
        if status:
            # Iterate though games
            # Go left
            if button == Controller.BTN_LEFT:
                self.game_idx += 1
                # fixes overshoot
                if self.game_idx >= len(PREVIEWS):
                    self.game_idx = 0
                self.__display_image(self.game_idx)
            # Go right
            elif button == Controller.BTN_RIGHT:
                self.game_idx -= 1
                # fixes overshoot
                if self.game_idx < 0:
                    self.game_idx = len(PREVIEWS) - 1
                self.__display_image(self.game_idx)
            # Starts games
            elif button == Controller.BTN_START:
                # Pong / first game
                if self.game_idx == 0:
                    self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, Colors.OFF)
                    self.scene_controller.load_scene(PongScene.PongScene())

    # loads the image and sets the game index to start value
    def reload(self):
        self.game_idx = 0
        self.__display_image(self.game_idx)

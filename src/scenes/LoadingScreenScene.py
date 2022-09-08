from config import Colors
from core.scenery.SceneBase import SceneBase
from core.scenery.SceneController import SceneController
from core.util.Player import Player
from core.rendering.renderer.RendererBase import RendererBase
from PIL import Image
import config.Config as Cfg
from config import ControllerKeys as Keys
from core.util.Vector2D import Vector2D
from scenes.snake import SnakeScene
from scenes.tetris import TetrisScene
import scenes.pong.PongScene as PongScene
from core.scenery.GameScene import GameScene

GAMES = [TetrisScene.TetrisScene(), SnakeScene.SnakeScene()]
START_KEYS = [Keys.BTN_START, Keys.BTN_SELECT, Keys.BTN_A]
ARROW_COLOR = Colors.WHITE
ARROW = "rsc//previews//arrow.png"
PREVIEWS = ["rsc//previews//tetris", "rsc//previews//snake"]


class LoadingScreenScene(SceneBase):
    images: []
    arrow_positions: [Vector2D[int], Vector2D[int]]
    game_idx: int

    def __init__(self, pre_scene: GameScene = None):
        super().__init__()

        self.images = []
        self.game_idx = 0

        if pre_scene in GAMES:
            self.game_idx = GAMES.index(pre_scene)

    def get_time_constant(self):
        return 1

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)
        self.scene_controller = scene_controller
        self.arrow_positions = []

        self.__generate_arrow_positions()
        self.__load_images()

        if len(self.images) != 0:
            self.__display_image(self.game_idx)
        else:
            print("Could not fine a preview image fitting for the screen")

    # no updates needed
    def on_update(self):
        pass

    def on_player_input(self, player: Player, button: int, status: bool):
        if status:
            # Iterate though scenes
            # Go left
            if button == Keys.BTN_LEFT:
                self.game_idx += 1
                # fixes overshoot
                if self.game_idx >= len(PREVIEWS):
                    self.game_idx = 0
                self.__display_image(self.game_idx)
            # Go right
            elif button == Keys.BTN_RIGHT:
                self.game_idx -= 1
                # fixes overshoot
                if self.game_idx < 0:
                    self.game_idx = len(PREVIEWS) - 1
                self.__display_image(self.game_idx)
            # Starts scenes
            elif button in START_KEYS:
                self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, Colors.OFF)
                if self.game_idx in range(len(GAMES)):
                    self.scene_controller.load_scene(GAMES[self.game_idx])

    # Generates the arrow overlay for the previews
    def __generate_arrow_positions(self):
        arrow = Image.open(ARROW)
        # Iterates through every pixel of the arrow and maps its desired positions relative to the screen
        for x in range(1, arrow.size[0] + 1):
            for y in range(arrow.size[1]):
                if arrow.getpixel((x - 1, y)):
                    pos_y = self.renderer.screen.size_y + 1 - int(arrow.size[1] / 2) - y
                    self.arrow_positions.append(Vector2D[int](x, pos_y))
                    self.arrow_positions.append(Vector2D[int](self.renderer.screen.size_x - x - 1, pos_y))

    def __display_image(self, idx: int):
        t_img = self.images[idx]
        # iterates through every pixel and displays the pixels colour at its position
        for x in range(t_img.size[0]):
            for y in range(t_img.size[1]):
                color = t_img.getpixel((x, y))[0:3]
                if Vector2D[int](x, y) in self.arrow_positions:
                    color = ARROW_COLOR
                self.renderer.set_led(x, t_img.size[1] - y - 1, color)
        self.renderer.push_leds()

    # Loads images
    def __load_images(self):
        for preview in PREVIEWS:
            # searches for the preview with equal size
            preview += str(self.renderer.screen.size_x)
            preview += "x"
            preview += str(self.renderer.screen.size_y)
            preview += ".png"
            try:
                self.images.append(Image.open(preview))
            except:
                pass

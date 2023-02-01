from PIL import Image
import math

import config.Config as Cfg
from config import Colors
from config import ControllerKeys as Keys
from core.scenery.SceneBase import SceneBase
from core.scenery.SceneController import SceneController
from core.util.Player import Player
from core.util.Vector2D import Vector2D
from core.rendering.renderer.RendererBase import RendererBase
from core.scenery.GameScene import GameScene

from scenes.drawing.DrawScene import DrawScene
from scenes.drawing.RGB_Spiral import RGB_Spiral
from scenes.snake import SnakeScene
from scenes.tetris import TetrisScene
from scenes.minesweeper.MinesweeperScene import MinesweeperScene

# List with instances of every scene that has a preview
SCENES = {
    "tetris": TetrisScene.TetrisScene(),
    "snake": SnakeScene.SnakeScene(),
    "minesweeper": MinesweeperScene(),
    "draw": DrawScene(),
    "RGB_Spiral": RGB_Spiral()
}

# Keys to use for starting the selected scene
START_KEYS = [Keys.BTN_START, Keys.BTN_SELECT, Keys.BTN_A]
# Color of the arrow
ARROW_COLOR = Colors.WHITE

# Resource-locations
ARROW = "rsc//previews//arrow.png"
PREVIEW_PATHS = "rsc//previews"


class LoadingScreenScene(SceneBase):
    # Preview-Images for the scenes (May contain an image for a scene or may not (Depending on if one exists)
    scene_images: {}
    # Name of the scene currently selected (Is a key of the global SCENES variable)
    scene_name: str

    arrow_images: [Image, Image]

    def __init__(self, pre_scene: GameScene = None):
        super().__init__()

        # Gets the currently selected game-name (If one got selected) or the default game
        self.scene_name = (
            list(SCENES.keys())[list(SCENES.values()).index(pre_scene)]
            if pre_scene is not None else
            list(SCENES.keys())[0]
        )

    def get_time_constant(self):
        return 1

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)
        self.scene_controller = scene_controller
        self.__generate_arrows()
        self.__load_images()

        # Displays the image if it could be found for the given scene
        self.__display_image()

    def on_update(self):
        pass

    def on_player_input(self, player: Player, button: int, status: bool):
        # Only acts on pulldown
        if not status:
            return

        # Checks for a start-press
        if button in START_KEYS:
            # Clears the screen
            self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, Colors.OFF)

            # Gets the selected scene and loads it
            self.scene_controller.load_scene(SCENES[self.scene_name])

        # Checks for a left/right arrow button
        if button in [Keys.BTN_LEFT, Keys.BTN_RIGHT]:
            # Gets the direction as -1 or 1
            direction = 1 if button == Keys.BTN_RIGHT else -1

            # Gets the keys of the scenes
            keys = list(SCENES.keys())

            # Gets the next index from the selected scene
            idx = keys.index(self.scene_name) + direction

            # Clamps the index
            if idx < 0:
                idx = len(keys) - 1
            if idx >= len(keys):
                idx = 0

            # Updates the selected scene
            self.scene_name = keys[idx]

            # Rerenders the screen
            self.__display_image()

    # Generates the arrow overlay for the previews and also it's mirror overlay
    def __generate_arrows(self):
        arrow = Image.open(ARROW)
        mirror = arrow.transpose(Image.FLIP_LEFT_RIGHT)

        self.arrow_images = [arrow, mirror]

    def __render_arrows(self):

        # Image width
        img_x = self.arrow_images[0].size[0]

        # Screen size
        sx = self.renderer.screen.size_x

        # Calculates the theoretically perfect space between all elements
        space = (sx - img_x * 2) / 3

        # Rounds down the perfect space for the borders
        space_border = int(space)
        # Rounds up the perfect space for the middle between the arrows
        space_between = math.ceil(space)

        # Renders the arrows
        self.renderer.image(self.arrow_images[0], space_border, 1)
        self.renderer.image(self.arrow_images[1], space_border + space_between + img_x, 1)

    '''
    Displays the image for the currently selected scene-name (If that image exists)
    '''

    def __display_image(self):
        self.renderer.clear_screen()

        # Ensures an image for the current scene exists
        if self.scene_name not in self.scene_images:
            # Renders the arrow
            self.__render_arrows()

            # Sends the led-update
            self.renderer.push_leds()
            return

        # Gets the image
        img = self.scene_images[self.scene_name]

        # Renders it
        self.renderer.image(img, 0, 0)

        # Renders the arrow
        self.__render_arrows()

        # Sends the led-update
        self.renderer.push_leds()

    # Loads images
    def __load_images(self):
        self.scene_images = {}

        # Iterates over every scene to check
        for scene_name in SCENES:
            # Creates the filename
            file_name = "{path}//{scene}{x}x{y}.png".format(path=PREVIEW_PATHS, scene=scene_name,
                                                            x=self.renderer.screen.size_x,
                                                            y=self.renderer.screen.size_y)
            try:
                # Tries to load that image
                self.scene_images[scene_name] = Image.open(file_name)
            except:
                continue

from PIL import Image

import time

from config import Colors
from core.rendering.characters import NumberRenderer
from core.rendering.renderer.RendererBase import RendererBase
from core.scenery.GameScene import GameScene
from core.util.Color import Color
from core.util.Player import Player
from core.scenery.SceneController import SceneController
from core.util.Vector2D import Vector2D

DELAY_TIME = 250_000  # in ms


class GameEndScene(GameScene):
    reload_scene: any
    won_game = False
    high_score = None
    init_time: int

    # only used to set an optional high score
    def __init__(self, high_score=None):
        if high_score:
            if type(high_score) != int:
                raise ValueError("non integer numbers are not supported yet")
            if high_score < 0:
                raise ValueError("negative numbers are not supported yet")

            self.high_score = high_score

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)

        self.renderer.fill(0, 0, renderer.screen.size_x, renderer.screen.size_y, Colors.OFF)
        self.renderer.start_capture_for_fade_in()

        self.init_time = time.time_ns() + 1000 * DELAY_TIME

        # when the player(s) loose
        if not self.won_game:
            try:
                img = Image.open("rsc//vfx//skull" + str(self.renderer.screen.size_x) + "x" + str(
                    self.renderer.screen.size_y) + ".png")

                # Displays the high score
                if self.high_score:
                    no_numbers_max = self.renderer.screen.size_x // NumberRenderer.DIMENSIONS_MIN.x
                    diff = self.renderer.screen.size_x - no_numbers_max * NumberRenderer.DIMENSIONS_MIN.x

                    screen_center = Vector2D(self.renderer.screen.size_x // 2, self.renderer.screen.size_y // 2)

                    score_position = Vector2D(
                        screen_center.x - len(str(self.high_score)) * NumberRenderer.DIMENSIONS_MIN.x // 2 + diff // 2,
                        screen_center.y - NumberRenderer.DIMENSIONS_MIN.y // 2)

                    num_renderer = NumberRenderer.NumberRenderer(pos=score_position, color=Color(255, 255, 255))
                    screen_buffer = num_renderer.render(self.high_score, renderer=self.renderer, return_as_array=True)

                    for x in range(self.renderer.screen.size_x):
                        for y in range(self.renderer.screen.size_y):
                            color = screen_buffer[x][y]
                            color += Color(205, 44, 44) if img.getpixel((x, img.size[1] - y - 1))[:3] != (
                            0, 0, 0) else Color(0, 0, 0)
                            self.renderer.set_led(x, y, color.rgb())
                else:
                    self.renderer.image(img, 0, 0)
            except FileNotFoundError:
                self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, Colors.RED)

            """# calculates a ray between the corners
            thickness = 1
            def ray(x: int): return int(x * self.renderer.screen.size_y / self.renderer.screen.size_x)
            if self.renderer.screen.size_y % 2 == 0 or self.renderer.screen.size_x % 2 == 0:
                def ray(x: int): return int(x * (self.renderer.screen.size_y + 1) / self.renderer.screen.size_x)
                thickness += int(ray(100)/100)

            # draws the ray from down left to up right and up left to down right
            for i in range(self.renderer.screen.size_x):
                for j in range(thickness):
                    j = j - int(thickness/2)
                    self.renderer.set_led(i, ray(i) + j, Colors.RED)
                    self.renderer.set_led(i, self.renderer.screen.size_y - 1 - j - ray(i), Colors.RED)"""

        # when the player(s) won
        else:
            self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, Colors.OFF)
            try:
                img = Image.open("rsc//vfx//tick" + str(self.renderer.screen.size_x) + "x" + str(
                    self.renderer.screen.size_y) + ".png")
                self.renderer.image(img, 0, 0)
            except:
                self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, Colors.GREEN)

        self.renderer.play_fade_in()
        
    def get_time_constant(self):
        return .1

    def on_player_input(self, player: Player, button: int, status: bool):

        if self.on_handle_loading_screen(button, status, self.reload_scene):
            return

        # Only acts on button up
        if status:
            return

        if time.time_ns() > self.init_time:
            self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, Colors.OFF)
            self.scene_controller.load_scene(self.reload_scene)

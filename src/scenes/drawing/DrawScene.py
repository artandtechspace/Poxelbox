import math

from core.scenery.GameScene import GameScene
from core.util.Player import Player
from core.util.Vector2D import Vector2D
from core.scenery.SceneController import SceneController
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerKeys as Controller
import colorsys
from random import randint as rint


class Point(Vector2D):
    # Weight of the given point
    weight: int

    def __init__(self, x: int, y: int, weight: int):
        super().__init__(x, y)
        self.weight = weight


class DrawScene(GameScene):
    points: [Point] = [Point(4, 4, 5)]
    timer: int = 0

    timer_speed: int = 1
    color_length: float = .5
    color_offset: float = .5
    pt_amt: int = 0
    pt_size_min: int = 3
    pt_size_max: int = 8

    def get_time_constant(self):
        return .1  # ms

    def on_player_input(self, player: Player, button: int, status: bool):

        # Handles the loading screen
        if super().on_handle_loading_screen(button, status):
            return

        if status:
            return

        # Checks if the key is correct to increment/decrement the timer-speed
        if button in [Controller.BTN_UP, Controller.BTN_DOWN]:
            self.timer_speed += 1 if Controller.BTN_UP == button else -1
            # Clamps between one and ten
            if self.timer_speed < 1:
                self.timer_speed = 1
            if self.timer_speed > 100:
                self.timer_speed = 100

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)

        self.points.clear()
        self.timer = 0
        self.pt_amt = rint(self.pt_size_min, self.pt_size_max)

        for i in range(self.pt_amt):
            self.add_random_point()

    # Returns the smallest distance to the nearest point of the given parameter-coordinate
    def get_distance_and_point(self, x: int, y: int):
        # Contains the smallest distance to the nearest point (So at first an infinitly large number)
        dist = 99999
        ret_pt = None

        for pt in self.points:
            # Distances to the points
            d_x_pt = pt.x - x
            d_y_pt = pt.y - y

            # Gets the distance to that point
            dist_to_pt = math.sqrt(d_x_pt * d_x_pt + d_y_pt * d_y_pt) / pt.weight

            # Checks if the distance is lower than the previous one
            if dist_to_pt < dist:
                dist = dist_to_pt
                ret_pt = pt

        return ret_pt, dist

    def on_update(self):
        self.timer += self.timer_speed

        if self.timer > 1000:
            self.timer = 0

        for pt in self.points:
            pt.weight -= .05
            if pt.weight <= 2:
                self.points.remove(pt)
                # Generates a new point
                self.add_random_point()

        self.render_scene()

    def add_random_point(self):
        self.points.append(
            Point(rint(0, self.renderer.screen.size_x), rint(0, self.renderer.screen.size_y), rint(3, 8)))

    def get_random_x_y_color(self, x: int, y: int):
        return (x ^ y) / 10 + self.timer / 1000

    def render_scene(self):

        for y in range(self.renderer.screen.size_y):
            for x in range(self.renderer.screen.size_x):
                pt, dist = self.get_distance_and_point(x, y)

                if dist > 1:
                    value = self.get_random_x_y_color(x, y)
                    bright = .4
                else:
                    value = dist * self.color_length + self.timer / 1000 + pt.weight / self.pt_size_max
                    bright = .6
                while value > 1:
                    value -= 1

                self.renderer.set_led(x, y, self.hsl_to_rgb(value, 1, bright))

        # Sends the update
        self.renderer.push_leds()

    def hsl_to_rgb(self, h: float, s: float, l: float):
        r, g, b = colorsys.hls_to_rgb(h, l, s)

        return r * 255, g * 255, b * 255

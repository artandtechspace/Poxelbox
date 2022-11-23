import math
import colorsys
from core.scenery.GameScene import GameScene
from core.util.Player import Player
from config import Colors
from core.scenery.SceneController import SceneController
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerKeys as Controller


def __find_parabola__(limits: [float], step_size=1, precision=5):
    """
    Finds an optimised weight for weight * x² with the limits = (Minima, Maxima),
    where weight * Minima² <= 1 and weight * Maxima² <= 0

    :param limits: (Minima, Maxima)
    :param step_size: step size by which the weight gets adjusted
    :param precision: how many times the step size gets reduced to 10% of itself
    :return: optimised weight
    """

    param = 0.1
    # gets the param to fit in the limits of the step size,
    # reducing it after each iteration to reduce needed calculations
    for i in range(precision):

        # Calculates max. term
        if limits[0] != 0:
            while param * limits[0] ** 2 < 1:
                param += step_size
            # overshoot by one => undo
            param -= step_size

        # checks if the end fits
        if limits[1] != 0:
            while param * limits[1] ** 2 < 0:
                param += step_size

        # adjust step size
        step_size = step_size / 10

    return param


def __adjust_variable__(value: float, step_size: float, increment: bool, limits: [float]):
    """
    Adjustment of a value based on following parameters

    :param value: starting value
    :param step_size: amount to in- or decrement
    :param increment: if step_size should be added or subtracted to value
    :param limits: (Minima, Maxima)
    :return: adjusted value
    """

    # in- or decrement
    value += step_size if increment else -step_size

    # correction when out of bounds
    if value <= limits[0] or value >= limits[1]:
        value -= step_size if increment else -step_size

    return value


class RGB_Spiral(GameScene):
    max_distance: float

    upper_limit: float
    lower_limit: float
    upper_gradient: float
    lower_gradient: float

    phase_shift: float
    d: float
    update_time: float
    speed: float
    mode: int

    def get_time_constant(self):
        return self.update_time  # ms

    def on_player_input(self, player: Player, button: int, status: bool):
        # Handles the loading screen
        if super().on_handle_loading_screen(button, status):
            return

        # aborts if no button is pressed
        if not status:
            return

        # Controller interaction
        # Checks if the key is correct to increment/decrement the speed
        self.update_time -= 0.05 if button == Controller.BTN_DOWN and self.update_time - 0.05 > 0 else 0
        self.update_time += 0.05 if button == Controller.BTN_UP else 0

        # upper limit adjust
        if button in [Controller.BTN_RIGHT, Controller.BTN_LEFT]:
            print('self.mode: ', self.mode)
            # Adjust upper limit
            if self.mode == 0:
                self.upper_limit = __adjust_variable__(self.upper_limit, 0.05, button == Controller.BTN_RIGHT,
                                                       (self.lower_limit, 1))
                # recalculate gradient
                self.upper_gradient = __find_parabola__((self.upper_limit - 1, 0))

            # Adjust lower limit
            elif self.mode == 1:
                self.lower_limit = __adjust_variable__(self.lower_limit, 0.05, button == Controller.BTN_RIGHT,
                                                       (0.05, self.upper_limit))
                # recalculate gradient
                self.lower_gradient = __find_parabola__((self.lower_limit, 0))

            # adjust d
            elif self.mode == 2:
                self.d = __adjust_variable__(self.d, 0.025, button == Controller.BTN_RIGHT,
                                             (-5, 5))

            # adjust the speed
            elif self.mode == 3:
                self.speed = __adjust_variable__(self.speed, 0.01, button == Controller.BTN_RIGHT,
                                                 (-5, 5))

        # mode adjustment
        if button in [Controller.BTN_A, Controller.BTN_B]:
            # increment or decrement the mode
            self.mode += 1 if button == Controller.BTN_A else -1

            # corrects when the mode is out of bounds
            self.mode = 0 if self.mode > 3 else self.mode
            self.mode = 3 if self.mode < 0 else self.mode

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)

        # starting with a black screen
        self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, Colors.OFF)
        self.renderer.push_leds()
        self.max_distance = math.sqrt((self.renderer.screen.size_y / 2) ** 2 +
                                      (self.renderer.screen.size_x / 2) ** 2)
        # variables
        self.phase_shift = 0
        self.d = 0.65
        self.mode = 0
        self.update_time = 0.1
        self.speed = 0.05

        # limits and gradients
        self.upper_limit = 0.7
        self.lower_limit = 0.4
        # calculate gradients
        self.lower_gradient = __find_parabola__((self.lower_limit, 0))
        self.upper_gradient = __find_parabola__((self.upper_limit - 1, 0))

    def on_update(self):
        for row in range(self.renderer.screen.size_y):
            for colum in range(self.renderer.screen.size_x):
                # x, y = distance form center on the corresponding axis
                x = colum - self.renderer.screen.size_x / 2
                y = row - self.renderer.screen.size_y / 2

                '''
                hue = arc-tan(y/x) * d + phase shift
                phase shift controls the change in color, based on time
                d controls the amount of same colored parts of the spiral
                arc-tan (y / x) = angel of the center to the coordinates
                '''
                hue = math.atan((y / x if x != 0 else 0)) * self.d + self.phase_shift
                # sets the LED to its corresponding color
                self.renderer.set_led(int(colum), int(row), self.dd_to_rgb(
                    hue=hue, distance=math.sqrt(x ** 2 + y ** 2)))
        # increases phase shift -> rotation movement of the colors
        self.phase_shift += self.speed

        self.renderer.push_leds()

    def dd_to_rgb(self, hue: float, distance: float):
        # calibrate inputs
        # refit hue
        hue = hue * 100 * 3.6 % 360
        while hue < 0:
            hue += 360
        while hue >= 360:
            hue -= 360
        # calculate the distance relative to the maximal distance
        x = distance / self.max_distance

        # HSV Color values
        if 0 < x < self.lower_limit:
            value = 1
            # S should go from 0 to 1
            saturation = self.lower_gradient * x ** 2
        elif self.lower_limit <= x < self.upper_limit:
            value = 1
            saturation = 1
        else:
            # S and V should go from 1 to 0
            value = self.upper_gradient * (x - 1) ** 2
            saturation = value

        color = colorsys.hsv_to_rgb(hue, saturation, value)
        for i in range(len(color)):
            color[i] *= 255
        return color

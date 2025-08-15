from core.rendering.Screen import Screen
from core.util.Vector2D import Vector2D
import config.Config as Cfg

import time
from PIL import Image

# temp
class configuration:
    RENDERER_FADE_IN_FRAMES: int = 30
    RENDERER_FADE_IN_DURATION: float = 1 # in seconds
    # in range [0, 1] where 0 ~ black; 1 ~ unchanged color
    RENDERER_SCALED_BRIGHTNESS_MAXVALUE: float = 0.5

#region Helperfunctions
@staticmethod
def lerp( color_a: (int, int, int), color_b: (int, int, int), t: float ):
    return tuple( int(a * (1-t) + b * t) for a, b in zip(color_a, color_b) )

@staticmethod
def set_color_brightness(color: (int, int, int), brightness: float):
    # conceptually the same as: 
    # return lerp( (0, 0, 0), color, brightness )
    return tuple( int(b * brightness) for b in color )

@staticmethod
def clamp(lower_bound, upper_bound, value):
    return min( lower_bound, max(upper_bound, value))
#endregion


class RendererBase:
    # Screen with some properties
    screen: Screen

    _is_capturing_screen : bool = False
    _caputured_set_led_calls: [int] = []

    def __init__(self):
        pass

    def setup(self):
        if not Cfg.BOX_HORIZONTAL:
            self.screen = Screen(Cfg.BOX_SIZE_X * Cfg.WALL_SIZE_X, Cfg.BOX_SIZE_Y * Cfg.WALL_SIZE_Y)
        else:
            self.screen = Screen(Cfg.BOX_SIZE_Y * Cfg.WALL_SIZE_X, Cfg.BOX_SIZE_X * Cfg.WALL_SIZE_Y)

    def clear_screen(self):
        self.fill(0,0,self.screen.size_x,self.screen.size_y, (0,0,0))

    def fill(self, vector1, vector2):
        pass

    # Fills the pixels from start to end with the given color (May be overriden with better code inside the specific renderer)
    def fill(self, start_x: int, start_y: int, width: int, height: int, color: (int, int, int)):
        for x in range(width):
            for y in range(height):
                self.set_led(x + start_x, y + start_y, color)
        pass

    '''
    Used to render rgba-images into the screen
    This cant handle transparency well but if an
    image has pixels with a transparency of 0, these pixels wont be rendered
    '''
    def image(self, img: Image, x_start: int, y_start: int):
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                color = img.getpixel((x, y))
                if color[3] > 0:
                    self.set_led(x+x_start, img.size[1] - y - 1 + y_start, (color[0], color[1], color[2]))

    '''
    Starts the capture for a fade-in.
    All calls to set_led will be saved and not executed.
    The capture ends when calling play_fade_in
    '''
    def start_capture_for_fade_in(self):
        self._caputured_set_led_calls = []
        self._is_capturing_screen = True
    
    '''
    Starts playback of a fade-in.
    End capture of set_led calls
    '''
    def play_fade_in(self):
        if not (self._is_capturing_screen and self._caputured_set_led_calls):
            return
        self._is_capturing_screen = False
        sleep_duration = configuration.RENDERER_FADE_IN_DURATION / configuration.RENDERER_FADE_IN_FRAMES
        for i in range(configuration.RENDERER_FADE_IN_FRAMES):
            for caputured_call in self._caputured_set_led_calls:
                self.set_led(
                        caputured_call[0],
                        caputured_call[1],
                        set_color_brightness(
                            caputured_call[2],
                            i/configuration.RENDERER_FADE_IN_FRAMES * i/configuration.RENDERER_FADE_IN_FRAMES
                        )
                )
            self.push_leds()
            time.sleep(sleep_duration)
        self._caputured_set_led_calls = []
    
    def set_led(self, x: int, y: int, color: (int, int, int)):
        """
        in child overrides:
        color = super(x, y, color) # brightess adjusted color
        if not color: # fade in abort
            return
        """
        if self._is_capturing_screen:
            # NOTE does override old capture when set_led is called on the same coordinate
            self._caputured_set_led_calls.append((x, y, color))
            return False
        return set_color_brightness(color=color, brightness=configuration.RENDERER_SCALED_BRIGHTNESS_MAXVALUE)

    def set_led_vector(self, vector: Vector2D[int], color):
        self.set_led(vector.x, vector.y, color)

    def push_leds(self):
        pass

from core.rendering.Screen import Screen
from core.util.Vector2D import Vector2D
import config.Config as Cfg
from PIL import Image


class RendererBase:
    # Screen with some properties
    screen: Screen

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

    def set_led(self, x: int, y: int, color: (int, int, int)):
        pass

    def set_led_vector(self, vector: Vector2D[int], color):
        self.set_led(vector.x, vector.y, color)

    def push_leds(self):
        pass

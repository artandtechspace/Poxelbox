from PIL import Image

from core.rendering.characters.CharacterRendererBase import CharacterRendererBase
from core.util.Color import Color
from core.util.Vector2D import Vector2D
from core.rendering.renderer.RendererBase import RendererBase

FONT_PATH = 'rsc//characters//'
DIMENSIONS_MIN = Vector2D(3, 5) + Vector2D(1, 1)  # = NumberRenderer.size + NumberRenderer.padding


class NumberRenderer(CharacterRendererBase):
    size = Vector2D(3, 5)
    padding = Vector2D(1, 1)
    color: Color(255, 255, 255)
    scale = 1
    auto_line_break = False

    def __init__(self, pos: Vector2D, scale=0, color=None, auto_line_break=None):
        super(NumberRenderer, self).__init__(pos)

        if color:
            if len(color) != Color:
                raise ValueError("color must be a color value")
            self.color = color

        if scale:
            if scale < 1:
                raise ValueError("scale is not allowed to be smaller than one")
            if type(scale) != int:
                raise ValueError("scale must be a whole number")
            self.scale = scale
            self.size *= scale

        if auto_line_break:
            if type(auto_line_break) != bool:
                raise ValueError("auto_line_break must be a boolean")
            self.auto_line_break = auto_line_break

    def render(self, number: int, renderer: RendererBase, return_as_array=False):
        if type(number) != int:
            raise ValueError("non integer numbers are not supported yet")
        if number < 0:
            raise ValueError("negative numbers are not supported yet")
        return_array = [[0 for y in range(renderer.screen.size_y)] for x in range(renderer.screen.size_x)]

        for char in str(number):
            t_img = Image.open(char + '.png')
            for x in range(self.size.x):
                for y in range(self.size.y):
                    if t_img.getpixel((x // self.scale, y // self.scale)):
                        if 0 < x + self.pos.x <= renderer.screen.size_x and \
                           0 < y + self.pos.y <= renderer.screen.size_y:
                            if return_as_array:
                                return_array[x + self.pos.x][y + self.pos.y] = self.color
                            else:
                                renderer.set_led(x + self.pos.x, y + self.pos.y, self.color)
                        else:
                            print("Current position:", str(self.pos))
                            raise Exception("Number is too large to be displayed at this position")
            self.pos += Vector2D(self.size.x, 0)
            self.__line_break(renderer.screen.size_x)
            self.pos += Vector2D(self.padding.x, 0)
            self.__line_break(renderer.screen.size_x)

        if return_as_array:
            return return_array

    def __line_break(self, max_x, min_y=0):
        if self.pos.x > max_x:
            if self.pos.y - self.size.y - self.padding.y > min_y:
                self.pos = Vector2D(0, self.pos.y - self.size.y - self.padding.y)
            else:
                print("Current position:", str(self.pos))
                raise Exception("Number is too large to be displayed at this position")

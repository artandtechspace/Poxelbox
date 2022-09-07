
from core.util.Vector2D import Vector2D
from numpy import array
from games.tetris.DefinedTetrisStuff import DEFINED_SHAPES
from core.rendering.renderer.RendererBase import RendererBase
from config import Colors
from games.tetris.DefinedTetrisStuff import BACKGROUND_COLOR

class Block:
    relative_coordinates: [[int]]
    shape_id: int
    position: Vector2D

    def __init__(self, shape_id: int, x: int, y: int):
        self.shape_id = shape_id
        self.relative_coordinates = array(DEFINED_SHAPES[shape_id].coords)
        self.position = Vector2D(x, y)

    # Flips the axes on all relative positions of the coordinates
    def __flip_axes(self):
        for cordIdx in range(len(self.relative_coordinates)):
            t_coordinate = self.relative_coordinates[cordIdx][1]
            self.relative_coordinates[cordIdx][1] = self.relative_coordinates[cordIdx][0]
            self.relative_coordinates[cordIdx][0] = t_coordinate

    '''
    Inverts all axes on the blocks coordinates

    :param use_x: if the x axis should be inverted, if false, this inverts the y axis
    '''

    def __invert_axes(self, use_x: bool):
        for cordIdx in range(len(self.relative_coordinates)):
            self.relative_coordinates[cordIdx][0 if use_x else 1] = -self.relative_coordinates[cordIdx][
                0 if use_x else 1]

    '''
    Rotates the block around itself.

    :param turn_left: if true, the piece will be rotated leftwise, if false rightwise
    '''

    # only edits the relative coordinates
    def rotate_block(self, turn_left: bool):
        self.__invert_axes(turn_left)
        self.__flip_axes()

    # Returns the color of the shape that the block has
    def get_color(self):
        return DEFINED_SHAPES[self.shape_id].color

    # Returns the shadow-color of the shape that the block has
    def get_shadow_color(self):
        return DEFINED_SHAPES[self.shape_id].shadow_color

    # Draws the block on the given renderer (If the erase-flag is set, the background color is used, otherwise the
    # shape-color)
    def display(self, renderer: RendererBase, do_erase: bool = False):
        for cord in self.relative_coordinates:
            abs_x = cord[0] + self.position.x
            abs_y = cord[1] + self.position.y
            renderer.set_led(abs_x, abs_y, BACKGROUND_COLOR if do_erase else self.get_color())

    def display_shadow(self, renderer: RendererBase, y_position: int, do_erase: bool = False):
        for cord in self.relative_coordinates:
            abs_x = cord[0] + self.position.x
            abs_y = cord[1] + y_position
            renderer.set_led(abs_x, abs_y, BACKGROUND_COLOR if do_erase else self.get_shadow_color())


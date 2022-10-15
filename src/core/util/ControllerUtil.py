from config import ControllerKeys as Keys
from core.rendering.Screen import Screen
from core.util.Vector2D import Vector2D

'''
Moves a given vector into the direction of the key (Only arrow-keys) and optionaly also clamps
this vector at the screens size if the parameter screen is given
'''


def move_into_direction(key: int, vec: Vector2D, screen: Screen = None):
    # Calculates the delta-position for x and y
    del_x = 1 if key == Keys.BTN_RIGHT else (-1 if key == Keys.BTN_LEFT else 0)
    del_y = 1 if key == Keys.BTN_UP else (-1 if key == Keys.BTN_DOWN else 0)

    # Sets the vectors values
    vec.x += del_x
    vec.y += del_y

    # If the vector should be clamped
    if screen is not None:
        if vec.x < 0 or vec.x >= screen.size_x:
            vec.x -= del_x
        if vec.y < 0 or vec.y >= screen.size_y:
            vec.y -= del_y

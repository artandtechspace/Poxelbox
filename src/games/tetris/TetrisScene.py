import time

from config import Colors
from core.util.Player import Player
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerKeys as Controller
from core.util.Vector2D import Vector2D
import random
from numpy import array
from core.scenery.SceneBase import SceneBase
from core.scenery.SceneController import SceneController

"""
A and B button to rotate blocks
Arrow keys to move blocks
"""

BACKGROUND_COLOR = Colors.OFF
GAME_OVER_COLOR = Colors.WHITE
O_block_color = Colors.YELLOW
I_block_color = Colors.CYAN
J_block_color = Colors.DARK_BLUE
L_block_color = Colors.ORANGE
S_block_color = Colors.GREEN
Z_block_color = Colors.RED
T_block_color = Colors.PURPLE

SHADOW_DIVIDER = 4


class Shape:
    coords: [[int]]
    color: (int, int, int)
    shadow_color: (int, int, int)

    def __init__(self, coords, color):
        self.color = color
        self.coords = coords

        self.__generate_shadow_color()

    # Takes the normal color and calculates the shadow-color
    def __generate_shadow_color(self):
        self.shadow_color = (
            self.color[0] / SHADOW_DIVIDER,
            self.color[1] / SHADOW_DIVIDER,
            self.color[2] / SHADOW_DIVIDER
        )


# Predefined shapes for the tetris blocks (With their colors)
DEFINED_SHAPES = (
    Shape([[0, 0], [1, 0], [0, -1], [1, -1]], O_block_color),
    Shape([[-1, 0], [0, 0], [1, 0], [2, 0]], I_block_color),
    Shape([[-1, -1], [-1, 0], [0, 0], [1, 0]], J_block_color),
    Shape([[-1, 0], [0, 0], [1, 0], [1, -1]], L_block_color),
    Shape([[-1, 0], [0, 0], [0, -1], [1, -1]], S_block_color),
    Shape([[-1, -1], [0, -1], [0, 0], [1, 0]], Z_block_color),
    Shape([[-1, 0], [0, 0], [0, -1], [1, 0]], T_block_color),
)

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


class TetrisScene(SceneBase):
    # Grid with the game_field
    game_field: [[int]]
    # Block that the player is holding
    current_block: Block
    # Node: Unused, theoretically a way to make the game faster
    game_speed: float
    # Used to give the player time after a respawn to move the block before the next game-tick
    spawn_counter: int
    # Flag used to prevent the player from moving already dropped pieces between ticks
    piece_got_dropped: bool = False

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)

        self.reset_game()

    def get_time_constant(self):
        return .1  # NOTE: Maybe change to self.game_speed

    def on_update(self):

        # Checks if the current piece is still in a spawn-delay
        if self.spawn_counter > 0:
            self.spawn_counter -= 1

            # Gameover check
            if self.spawn_counter == 0:
                # Checks if no low position could be found and therefor this is gameover
                if self.get_lowest_block_position() == self.current_block.position.y:
                    self.game_over()
            return

        # Drop-flag-reset
        self.piece_got_dropped = False

        # Checks if the next spot is not blocked
        if self.can_block_be_moved_to(self.current_block.position.x, self.current_block.position.y - 1):
            self.move_block(0, -1)
        else:
            self.place_block()
            self.clear_full_rows()
            self.generate_new_block()
            self.game_speed = self.game_speed / 2
            self.current_block.display_shadow(self.renderer, self.get_lowest_block_position())
            self.current_block.display(self.renderer)
        self.renderer.push_leds()

    def on_player_input(self, player: Player, button: int, status: bool):
        if not status or self.piece_got_dropped:
            return

        # Restricts move-down operations
        if self.spawn_counter > 0 and button in [Controller.BTN_DOWN, Controller.BTN_UP]:
            return

        # Simple movement buttons
        if button in [Controller.BTN_DOWN, Controller.BTN_LEFT, Controller.BTN_RIGHT]:
            # Relative X/Y movement
            rel_x = -1 if button == Controller.BTN_LEFT else (1 if button == Controller.BTN_RIGHT else 0)
            rel_y = -1 if button == Controller.BTN_DOWN else 0

            # Checks if the block can be moved and if so, lets it move
            if self.can_block_be_moved_to(self.current_block.position.x + rel_x, self.current_block.position.y + rel_y):
                self.move_block(rel_x, rel_y)
                self.renderer.push_leds()
            return

        # Dropping the block
        if button == Controller.BTN_UP:
            difference_to_fall = self.current_block.position.y - self.get_lowest_block_position()
            self.move_block(0, -difference_to_fall)
            self.piece_got_dropped = True

        # Spinning the blocks
        if button == Controller.BTN_A:
            self.rotate_block_if_possible(False)
        if button == Controller.BTN_B:
            self.rotate_block_if_possible(True)

        self.renderer.push_leds()

    # Resets the game back to its original state, so it can be (re)played
    def reset_game(self):
        self.game_field = [[-1 for x in range(self.renderer.screen.size_x)] for y in range(self.renderer.screen.size_y)]
        self.generate_new_block()
        self.game_speed = 0.1

    # Pseudo-Randomly generates a new block from the tetris-previews
    def generate_new_block(self):
        self.spawn_counter = 4
        self.current_block = Block(
            random.randint(0, len(DEFINED_SHAPES) - 1),
            int(self.renderer.screen.size_x / 2),
            self.renderer.screen.size_y
        )
        # tests if the block is outside the window and corrects it
        for cord in self.current_block.relative_coordinates:
            abs_y = cord[1] + self.current_block.position.y
            # Moves the pieces position as low as required to it into the screen
            while abs_y >= self.renderer.screen.size_y:
                self.current_block.position.y -= 1
                abs_y = cord[1] + self.current_block.position.y

    # Places the currently held block on the grid
    def place_block(self):
        for cord in self.current_block.relative_coordinates:
            abs_x = cord[0] + self.current_block.position.x
            abs_y = cord[1] + self.current_block.position.y
            self.game_field[abs_y][abs_x] = self.current_block.shape_id
            self.renderer.set_led(abs_x, abs_y, self.current_block.get_color())

    # Returns if the current block can be moved to the  given absolute coordinats without colliding with the grid or
    # it's walls
    def can_block_be_moved_to(self, x: int, y: int):
        # Checks every relative-coordinate of the block from the given position if it collides with anything on the
        # game-field
        for cord in self.current_block.relative_coordinates:
            abs_x = cord[0] + x
            abs_y = cord[1] + y

            # Checks if the x or y positions are moving off-screen or are colliding with any piece that is already
            # inside the game-field array
            if abs_x < 0 or abs_x >= self.renderer.screen.size_x or abs_y < 0 or abs_y >= self.renderer.screen.size_y or self.game_field[abs_y][abs_x] != -1:
                return False
        return True

    # Tries to rotate the block into the desired direction if possible. Return if the rotation was possible
    # This also un/re-renders the block
    def rotate_block_if_possible(self, turn_left: bool):
        # Rotates the block to check
        self.current_block.rotate_block(turn_left)

        # If the block can be rotated
        can_rotate = self.can_block_be_moved_to(self.current_block.position.x, self.current_block.position.y)

        # Undoes the rotation
        self.current_block.rotate_block(not turn_left)

        if not can_rotate:
            return False

        # Unrenders
        self.current_block.display_shadow(self.renderer, self.get_lowest_block_position(), True)
        self.current_block.display(self.renderer, True)

        # Rotates
        self.current_block.rotate_block(turn_left)

        # Re-renders
        self.current_block.display_shadow(self.renderer, self.get_lowest_block_position())
        self.current_block.display(self.renderer)

        return True

    # Removes all full-rows from the game-field, if there are any
    # and if so, rerenders the whole field
    def clear_full_rows(self):
        # Filters out every row where no unset block is left
        self.game_field = list(filter(lambda row: not all(elm > -1 for elm in row), self.game_field))

        # Calculates the amount of filtered rows
        amt = self.renderer.screen.size_y - len(self.game_field)

        # Appends as many empty row to get back to its original size
        self.game_field += [[-1 for _ in range(self.renderer.screen.size_x)] for _1 in range(amt)]

        # Checks if there were any changes
        if amt > 0:
            # Rerenders the whole game-grid
            for y in range(self.renderer.screen.size_y):
                for x in range(self.renderer.screen.size_x):
                    self.renderer.set_led(x, y,
                                          BACKGROUND_COLOR if self.game_field[y][x] == -1
                                          else DEFINED_SHAPES[self.game_field[y][x]].color)

    # Gets the lowest possible y-position that the current block can be moved to
    # If not lowest position could be found, this return none
    def get_lowest_block_position(self):
        y = self.current_block.position.y
        # Decrements the block position until it can no longer be moved
        while True:
            if self.can_block_be_moved_to(self.current_block.position.x, y-1):
                y -= 1
            else:
                break

        return y

    # Executes once the game is gameover for the player
    def game_over(self):
        # TODO: Implement better game-over-background
        self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, GAME_OVER_COLOR)
        self.renderer.push_leds()
        time.sleep(5)
        self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, BACKGROUND_COLOR)
        self.reset_game()

    def move_block(self, dx: int, dy: int):
        # Erases the shadow and block from the renderer
        self.current_block.display_shadow(self.renderer, self.get_lowest_block_position(), True)
        self.current_block.display(self.renderer, True)

        # Moves the piece
        self.current_block.position.x += dx
        self.current_block.position.y += dy

        # Renders the shadow and block
        self.current_block.display_shadow(self.renderer, self.get_lowest_block_position())
        self.current_block.display(self.renderer)

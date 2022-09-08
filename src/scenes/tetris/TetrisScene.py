import time

from core.util.Player import Player
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerKeys as Controller
import random
from core.scenery.GameScene import GameScene
from core.scenery.SceneController import SceneController
from scenes.GameOverScene import GameOverScene
from scenes.tetris.DefinedTetrisStuff import DEFINED_SHAPES
from scenes.tetris.DefinedTetrisStuff import BACKGROUND_COLOR
from scenes.tetris.Block import Block
import config.Config as Cfg

# Collision error codes
COLLISION_GRID = 1
COLLISION_WALL_RIGHT = 2
COLLISION_WALL_LEFT = 3
COLLISION_WALL_BOTTOM = 4
NO_COLLISION = 0

class TetrisScene(GameScene):
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
        self.scene_controller = scene_controller

        self.reset_game()

    def get_time_constant(self):
        return Cfg.TETRIS_SPEED  # NOTE: Maybe change to self.game_speed

    def on_update(self):

        if self.spawn_counter > 0:
            self.spawn_counter -= 1
            return

        # Drop-flag-reset
        self.piece_got_dropped = False

        # Checks if the next spot is not blocked
        if self.can_block_be_moved_to(self.current_block.position.x, self.current_block.position.y - 1) == NO_COLLISION:
            self.move_block(0, -1)
        else:
            self.place_block()
            self.clear_full_rows()
            self.generate_new_block()

            # Checks if the block is colliding with the grid
            if self.can_block_be_moved_to(self.current_block.position.x, self.current_block.position.y) != NO_COLLISION:
                self.game_over()
                return

            self.game_speed = self.game_speed / 2
            self.current_block.display_shadow(self.renderer, self.get_lowest_block_position())
            self.current_block.display(self.renderer)
        self.renderer.push_leds()

    def on_player_input(self, player: Player, button: int, status: bool):
        super().on_player_input(player, button, status)
        if not status or self.piece_got_dropped:
            return

        # Simple movement buttons
        if button in [Controller.BTN_DOWN, Controller.BTN_LEFT, Controller.BTN_RIGHT]:
            # Relative X/Y movement
            rel_x = -1 if button == Controller.BTN_LEFT else (1 if button == Controller.BTN_RIGHT else 0)
            rel_y = -1 if button == Controller.BTN_DOWN else 0

            # Checks if the block can be moved and if so, lets it move
            if self.can_block_be_moved_to(self.current_block.position.x + rel_x, self.current_block.position.y + rel_y) == NO_COLLISION:
                self.move_block(rel_x, rel_y)
                self.renderer.push_leds()
            return

        # Dropping the block
        if button == Controller.BTN_UP:
            difference_to_fall = self.current_block.position.y - self.get_lowest_block_position()
            self.move_block(0, -difference_to_fall)
            self.piece_got_dropped = True
            self.spawn_counter = 0

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

        # Renders the new block
        self.move_block(0, 0)
        self.renderer.push_leds()

    # Pseudo-Randomly generates a new block from the tetris-previews
    def generate_new_block(self):
        self.spawn_counter = 2
        self.current_block = Block(
            random.randint(0, len(DEFINED_SHAPES) - 1),
            int(self.renderer.screen.size_x / 2),
            self.renderer.screen.size_y
        )

    # Places the currently held block on the grid
    def place_block(self):
        for cord in self.current_block.relative_coordinates:
            abs_x = cord[0] + self.current_block.position.x
            abs_y = cord[1] + self.current_block.position.y

            # Checks if the position is inside the grid
            if abs_y < self.renderer.screen.size_y:
                self.game_field[abs_y][abs_x] = self.current_block.shape_id
                self.renderer.set_led(abs_x, abs_y, self.current_block.get_color())

    # Returns if the current block can be moved to the given absolute coordinats without colliding with the grid or
    # it's walls
    # Return COLLISION_... as an error code or 0 if the movement is possible
    def can_block_be_moved_to(self, x: int, y: int) -> int:
        # Checks every relative-coordinate of the block from the given position if it collides with anything on the
        # game-field
        for cord in self.current_block.relative_coordinates:
            abs_x = cord[0] + x
            abs_y = cord[1] + y

            # Checks x-left
            if abs_x < 0:
                return COLLISION_WALL_LEFT

            # Checks x-right
            if abs_x >= self.renderer.screen.size_x:
                return COLLISION_WALL_RIGHT

            # Checks y-axis
            if abs_y < 0:
                return COLLISION_WALL_BOTTOM

            # Checks grid
            if abs_y < self.renderer.screen.size_y and self.game_field[abs_y][abs_x] != -1:
                return COLLISION_WALL_BOTTOM

        return NO_COLLISION

    # Tries to rotate the block into the desired direction if possible. Return if the rotation was possible
    # This also un/re-renders the block
    def rotate_block_if_possible(self, turn_left: bool):
        # Rotates the block to check
        self.current_block.rotate_block(turn_left)

        # If the block can be rotated
        rotate_result = self.can_block_be_moved_to(self.current_block.position.x, self.current_block.position.y)

        # Direction the block must move to, if rotated and collided. This can be left 0 if no movement is required
        move_direction = 0

        # Checks if no rotation is possible
        if rotate_result != NO_COLLISION:
            # Checks if the collision is with the bottom
            if rotate_result == COLLISION_WALL_BOTTOM:
                # Undoes the rotation
                self.current_block.rotate_block(not turn_left)
                return False

            # Calculates the direction that the block must move to, to get away from the wall
            move_direction = -1 if rotate_result == COLLISION_WALL_RIGHT else 1

            # Checks if the rotated block can be placed if moved aside by one pixel
            if not self.can_block_be_moved_to(self.current_block.position.x + move_direction, self.current_block.position.y) == NO_COLLISION:
                # Undoes the rotation
                self.current_block.rotate_block(not turn_left)
                return False

        # Undoes the rotation
        self.current_block.rotate_block(not turn_left)

        # Un-renders
        self.current_block.display_shadow(self.renderer, self.get_lowest_block_position(), True)
        self.current_block.display(self.renderer, True)

        # Rotates
        self.current_block.rotate_block(turn_left)

        # Moves (If required)
        self.current_block.position.x += move_direction

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
    # If not the lowest position could be found, this return none
    def get_lowest_block_position(self):
        y = self.current_block.position.y
        # Decrements the block position until it can no longer be moved
        while True:
            if self.can_block_be_moved_to(self.current_block.position.x, y-1) == NO_COLLISION:
                y -= 1
            else:
                break

        return y

    # Executes once the game is game over for the player
    def game_over(self):
        game_end = GameOverScene()
        game_end.reload_scene = self
        self.scene_controller.load_scene(game_end)

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

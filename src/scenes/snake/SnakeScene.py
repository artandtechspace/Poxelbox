from config import Colors
from core.scenery.GameScene import GameScene
from core.util.Player import Player
from core.scenery.SceneController import SceneController
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerKeys as Controller
from random import random
from core.util.Vector2D import Vector2D
from scenes.GameEndScene import GameEndScene
import config.Config as Cfg

BACKGROUND_COLOR = Colors.OFF
BERRY_COLOR = Colors.MAGENTA
PLAYER_COLOR = Colors.YELLOW
PLAYER_COLOR_HEAD = Colors.ORANGE

# Control-pad-buttons
DIRECTION_BUTTON_MAPPINGS = {
    Controller.BTN_DOWN: Vector2D[int](0, -1),
    Controller.BTN_RIGHT: Vector2D[int](1, 0),
    Controller.BTN_LEFT: Vector2D[int](-1, 0),
    Controller.BTN_UP: Vector2D[int](0, 1),
}


class SnakeScene(GameScene):
    # Array with positions that the snake occupies
    snake_body: [Vector2D[int]]

    # Position of the berry which the snake must eat
    berry_pos: Vector2D[int]

    # Vector for the move direction of the snake
    direction: Vector2D[int] | None
    # Vector for the wanted next position of the snake
    wanted_direction: Vector2D[int] | None

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)
        self.scene_controller = scene_controller

        # Start head position of the snake
        start = Vector2D[int](int(self.renderer.screen.size_x / 2), int(self.renderer.screen.size_y / 2))

        self.snake_body = [
            # First three body positions
            start,
            start.copy_and_add(y=1),
            start.copy_and_add(y=2)
        ]
        # Finds the first berry pos
        self.reset_berry()
        # Sets the initial direction
        self.direction = self.wanted_direction = None

        # Performs first renders
        self.renderer.set_led_vector(self.berry_pos, BERRY_COLOR)
        for vec in self.snake_body:
            self.renderer.set_led_vector(vec, PLAYER_COLOR)
        self.renderer.set_led_vector(self.snake_body[-1], PLAYER_COLOR_HEAD)
        self.renderer.push_leds()

    def get_position_inside_wall(self, v: Vector2D[int]):
        """
        Checks and :returns: if the given position :param v: is inside a wall if the screen
        """
        # Checks right x
        if v.x >= self.renderer.screen.size_x:
            return 0b00

        # Checks upper y
        if v.y >= self.renderer.screen.size_y:
            return 0b10

        # Checks left x
        if v.x < 0:
            return 0b01

        # Checks lower y
        if v.y < 0:
            return 0b11

        # Didn't ran into a wall
        return None

    def is_snake_in_position(self, x: int, y: int):
        """
        Checks and :returns: if the given position :param x: :param y: is also occupied by the snake
        """

        # Iterates over every body position and checks the cords
        for vec in self.snake_body:
            if vec.x == x and vec.y == y:
                return True
        return False

    def start_game_over_sequence(self):
        """
        Starts the sequence to signal a game over
        """
        game_end = GameEndScene(high_score=len(self.snake_body) - 3)
        game_end.reload_scene = self
        self.scene_controller.load_scene(game_end)

    # Finds a new position for the berry
    def reset_berry(self):
        """
        Resets the berry to a new possible position
        :return:
        """

        # Firstly stores all possible positions by checking which the snake doesn't occupy
        possible_positions = [Vector2D[int]]
        for x in range(self.renderer.screen.size_x):
            for y in range(self.renderer.screen.size_y):
                if not self.is_snake_in_position(x, y):
                    possible_positions.append(Vector2D[int](x, y))

        # Checks if the berry has nowhere to go
        if len(possible_positions) == 0:
            # Just moves it out of screen
            self.berry_pos = Vector2D(-1, -1)
            return

        # Picks a position at random
        self.berry_pos = possible_positions[int(random() * len(possible_positions))]

    def get_time_constant(self):
        return Cfg.SNAKE_SPEED

    def on_player_input(self, player: Player, button: int, status: bool):
        # Handles the loading screen
        if super().on_handle_loading_screen(button, status):
            return

        if not status:
            return

        # Checks if a direction button got pressed
        if button in DIRECTION_BUTTON_MAPPINGS:
            self.wanted_direction = DIRECTION_BUTTON_MAPPINGS[button]

    def on_update(self):

        # The update algorithm goes as follows:
        # 0. Update direction if it doesn't lead to a game-over
        # 1. Checks for walls
        # 2. Checks for berry
        # 3. If no berry found, remove last tailpiece
        #    - If found let the piece stay
        # 4. Check for movement into itself

        # Checks if a new direction is wanted
        if self.wanted_direction is not None:
            # and if it makes sense (So doesn't kill the snake)
            possible_head = self.snake_body[-1] + self.wanted_direction

            would_die = self.is_snake_in_position(possible_head.x, possible_head.y)

            # If the wall-death is enabled, the wall position is considered bad
            if Cfg.SNAKE_WALL_DEAD:
                would_die |= self.get_position_inside_wall(possible_head) is not None

            if not would_die:
                self.direction = self.wanted_direction

            # Resets the wanted direction
            self.wanted_direction = None

        # Checks if the player hasn't started
        if self.direction is None:
            return

        # Get the next head position
        head: Vector2D[int] = self.snake_body[-1] + self.direction

        # Checks if the snake ran into a wall
        wall_pos = self.get_position_inside_wall(head)
        if wall_pos is not None:

            # If wall-death is enabled, play the death screen
            if Cfg.SNAKE_WALL_DEAD:
                self.start_game_over_sequence()
                return

            # Sets the head to the opposite direction
            # Checks bit for axis (0 is x)
            if (wall_pos >> 1) & 1 == 0:
                # Multiples the full length to get the correct new position
                head.x = (self.renderer.screen.size_x-1) * (wall_pos & 1)
            else:
                head.y = (self.renderer.screen.size_y-1) * (wall_pos & 1)

        # Checks if the berry got eaten
        if self.berry_pos == head:
            # Searches for a new berry
            self.renderer.set_led_vector(self.berry_pos, BACKGROUND_COLOR)
            self.reset_berry()
            self.renderer.set_led_vector(self.berry_pos, BERRY_COLOR)

            # Doesn't remove the tail
        else:
            # Removes the snake body
            self.renderer.set_led_vector(self.snake_body[0], BACKGROUND_COLOR)
            self.snake_body.pop(0)

        # Checks if the snake ran into itself
        if self.is_snake_in_position(head.x, head.y):
            self.start_game_over_sequence()
            return

        # Appends the new head
        self.renderer.set_led_vector(self.snake_body[-1], PLAYER_COLOR)
        self.snake_body.append(head)
        self.renderer.set_led_vector(head, PLAYER_COLOR_HEAD)

        # Sends the update
        self.renderer.push_leds()

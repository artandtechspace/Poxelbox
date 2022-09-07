from config import Colors
from core.scenery.SceneBase import SceneBase
from core.util.Player import Player
from core.scenery.SceneController import SceneController
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerKeys as Controller
from random import random
from core.util.Vector2D import Vector2D
from games.GameOverScene import GameOverScene

BACKGROUND_COLOR = Colors.OFF
BERRY_COLOR = Colors.MAGENTA
PLAYER_COLOR = Colors.YELLOW
PLAYER_COLOR_HEAD = Colors.ORANGE
PLAYER_START_LENGTH = 3

# Control-pad-buttons
CONTROL_PAD_BUTTONS = [Controller.BTN_RIGHT, Controller.BTN_LEFT, Controller.BTN_UP, Controller.BTN_DOWN]


class SnakeScene(SceneBase):
    pressed_button: int
    player_length: int
    player_head_pos: Vector2D[int]
    player_body_pos: [Vector2D[int]]
    berry_pos: Vector2D[int]
    moves: int
    direction: Vector2D

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)
        self.scene_controller = scene_controller

        self.restart()

    def restart(self):
        self.pressed_button = Controller.BTN_UP
        self.player_length = PLAYER_START_LENGTH
        self.moves = 0
        self.direction = Vector2D(0, 1)

        # paints the window
        self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, BACKGROUND_COLOR)

        self.player_head_pos = Vector2D[int](int(self.renderer.screen.size_x / 2), int(self.renderer.screen.size_y / 2))
        self.player_body_pos = []
        for segment in range(self.player_length - 1):
            segment = self.player_length - segment - 1
            self.player_body_pos.append(Vector2D[int](self.player_head_pos.x, (self.player_head_pos.y - segment)))
            self.renderer.set_led(self.player_body_pos[-1].x, self.player_body_pos[-1].y, PLAYER_COLOR)

        # first sets the berry
        self.find_new_berry()
        # fist draws the player
        self.draw_player_head()
        self.update_screen()

    def update_screen(self):
        self.renderer.push_leds()

    def draw_player_head(self):
        self.renderer.set_led(self.player_head_pos.x, self.player_head_pos.y, PLAYER_COLOR_HEAD)
        self.player_body_pos.append(self.player_head_pos.copy())

    def erase_player_tail(self):
        self.renderer.set_led(self.player_head_pos.x, self.player_head_pos.y, PLAYER_COLOR)
        player_tail_pos = self.player_body_pos[0]
        length_difference = self.player_length - len(self.player_body_pos)
        # if the snake is long enough, remove last pixel
        if length_difference <= 0:
            self.renderer.set_led_vector(player_tail_pos, BACKGROUND_COLOR)
            self.player_body_pos.pop(0)
        # if the snake is too short, keep last pixel
        elif length_difference > 0:
            pass

    # Returns if the players body occupies the given x/y position
    def does_player_occupy_position(self, x, y):
        # Iterates over every body position and checks the coords
        for vec in self.player_body_pos:
            if vec.x == x and vec.y == y:
                return True
        return False

    def find_new_berry(self):
        possible_positions = [Vector2D[int]]
        for x in range(self.renderer.screen.size_x):
            for y in range(self.renderer.screen.size_y):
                if not self.does_player_occupy_position(x, y):
                    possible_positions.append(Vector2D[int](x, y))
        possible_positions.pop(0)
        if len(possible_positions) == 0:
            # player is in every pixel
            self.won_screen()
            pass
        else:
            picked_position = int(random() * len(possible_positions))
            self.berry_pos = possible_positions[picked_position]
            self.renderer.set_led_vector(self.berry_pos, BERRY_COLOR)

    def won_screen(self):
        # TODO make a proper win screen
        self.restart()
        pass

    def player_eats_berry(self):
        self.player_length += 1

    def berry_mechanics(self):
        if self.berry_pos == self.player_head_pos:
            self.player_eats_berry()
            self.find_new_berry()

    def game_over(self):
        game_end = GameOverScene()
        game_end.reload_scene = self
        self.scene_controller.load_scene(game_end)

    def collision_detection_self(self):
        return self.does_player_occupy_position(self.player_head_pos.x, self.player_head_pos.y)

    def get_time_constant(self):
        return .15

    def on_player_input(self, player: Player, button: int, status: bool):
        if status:
            # go down
            if button == Controller.BTN_DOWN:
                self.direction = Vector2D(0, -1)
            # go up
            elif button == Controller.BTN_UP:
                self.direction = Vector2D(0, 1)
            # go left
            elif button == Controller.BTN_LEFT:
                self.direction = Vector2D(-1, 0)
            # go right
            elif button == Controller.BTN_RIGHT:
                self.direction = Vector2D(1, 0)

    def on_update(self):
        self.__move(self.direction)
        self.berry_mechanics()
        self.moves += 1
        self.update_screen()

    def __move(self, dv: Vector2D):
        # out of the screen detection
        if self.renderer.screen.size_x > self.player_head_pos.x + dv.x >= 0 and \
                self.renderer.screen.size_y > self.player_head_pos.y + dv.y >= 0:
            # not running in itself
            if self.player_head_pos.x + dv.x != self.player_body_pos[-2].x or\
               self.player_head_pos.y + dv.y != self.player_body_pos[-2].y:
                self.erase_player_tail()
                self.player_head_pos = self.player_head_pos + dv
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player_head()
            else:
                # would have run into self -> moves in the opposite as pressed direction
                self.__move(Vector2D(-dv.x, -dv.y))
        else:  # must be outside the borders
            self.game_over()

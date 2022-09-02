from config import Colors
from core.scenery.SceneBase import SceneBase
from core.util.Player import Player
from core.scenery.SceneController import SceneController
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerKeys as Controller
from random import random
from core.util.Vector2D import Vector2D

BACKGROUND_COLOR = Colors.OFF
BERRY_COLOR = Colors.MAGENTA
PLAYER_COLOR = Colors.YELLOW
PLAYER_START_LENGTH = 3

# Control-pad-buttons
CONTROLL_PAD_BUTTONS = [Controller.BTN_RIGHT, Controller.BTN_LEFT, Controller.BTN_UP, Controller.BTN_DOWN]

class SnakeScene(SceneBase):
    pressed_button: int
    player_length: int
    player_head_pos: Vector2D[int]
    player_body_pos: [Vector2D[int]]
    berry_pos: Vector2D[int]

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player, player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)

        self.restart()

    def restart(self):
        self.pressed_button = Controller.BTN_UP
        self.player_length = PLAYER_START_LENGTH
        self.player_head_pos = Vector2D[int](int(self.renderer.screen.size_x / 2), int(self.renderer.screen.size_y / 2))
        self.player_body_pos = [self.player_head_pos.copy()]

        # paints the window
        self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, BACKGROUND_COLOR)

        # first sets the berry
        self.find_new_berry()
        # fist draws the player
        self.draw_player()
        self.update_screen()

    def update_screen(self):
        self.renderer.push_leds()

    def draw_player(self):
        self.renderer.set_led(self.player_head_pos.x, self.player_head_pos.y, PLAYER_COLOR)
        self.player_body_pos.append(self.player_head_pos.copy())

    def erase_player(self):
        player_tail_pos = self.player_body_pos[0]
        length_difference = self.player_length - len(self.player_body_pos)
        if length_difference <= 0:
            self.renderer.set_led_vector(player_tail_pos, BACKGROUND_COLOR)
            self.player_body_pos.pop(0)
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
            picked_position = int(random()*len(possible_positions))
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
        # TODO: Refactor @Anton
        smaller_window_side = self.renderer.screen.size_x if self.renderer.screen.size_x <= self.renderer.screen.size_y else self.renderer.screen.size_y
        ray_y = lambda h: (h*self.renderer.screen.size_y/smaller_window_side)  # * 1 + self.start_pos[1]
        for i in range(smaller_window_side):
            self.renderer.fill(i, ray_y(i), 1, 1, (255, 0, 0))
            self.renderer.fill((self.renderer.screen.size_x-1-i), ray_y(i), 1, 1, (255, 0, 0))
        self.update_screen()
        self.restart()

    def collision_detection_self(self):
        return self.does_player_occupy_position(self.player_head_pos.x, self.player_head_pos.y)

    def get_time_constant(self):
        return .1

    def on_player_input(self, player: Player, button: int, status: bool):
        if status and button in CONTROLL_PAD_BUTTONS:
            self.pressed_button = button

    def on_update(self):
        if self.pressed_button == Controller.BTN_DOWN:
            if self.player_head_pos.y > 0:
                self.erase_player()
                self.player_head_pos.y -= 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else:  # must be outside the borders
                self.game_over()
        elif self.pressed_button == Controller.BTN_UP:
            if self.player_head_pos.y + 1 < self.renderer.screen.size_y:
                self.erase_player()
                self.player_head_pos.y += 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else:  # must be outside the borders
                self.game_over()
        elif self.pressed_button == Controller.BTN_LEFT:
            if self.player_head_pos.x > 0:
                self.erase_player()
                self.player_head_pos.x -= 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else:  # must be outside the borders
                self.game_over()
        elif self.pressed_button == Controller.BTN_RIGHT:
            if self.player_head_pos.x + 1 < self.renderer.screen.size_x:
                self.erase_player()
                self.player_head_pos.x += 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else:  # must be outside the borders
                self.game_over()
        self.berry_mechanics()
        self.update_screen()
        pass

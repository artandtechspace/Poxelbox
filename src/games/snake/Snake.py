from config import Colors
from games.GameBase import GameBase
from core.util.Player import Player
from core.GameController import GameController
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerKeys as Controller
from random import random

# constants
field_color = Colors.OFF
berry_color = Colors.MAGENTA
player_color = Colors.YELLOW
player_start_length = 3


class Snake(GameBase):
    pressed_button: int
    player_length: int
    player_head_pos: [int, int]
    player_body_pos: [(int, int)]
    berry_pos: [int, int]

    def init(self, game_controller: GameController, renderer: RendererBase, player_one: Player, player_two: Player):
        super().init(game_controller, renderer, player_one, player_two)

        self.restart()

    def restart(self):
        self.pressed_button = Controller.BTN_UP
        self.player_length = player_start_length
        self.player_head_pos = [int(self.renderer.screen.size_x/2), int(self.renderer.screen.size_y/2)]
        self.player_body_pos = [(self.player_head_pos[0], self.player_head_pos[1])]

        # paints the window
        for i in range(self.renderer.screen.size_x):
            for j in range(self.renderer.screen.size_y):
                self.renderer.fill(i, j, 1, 1, field_color)
        # first sets the berry
        self.find_new_berry()
        # fist draws the player
        self.draw_player()
        self.update_screen()

    def update_screen(self):
        self.renderer.push_leds()

    def draw_player(self):
        self.renderer.fill((self.player_head_pos[0]), (self.player_head_pos[1]), 1, 1, player_color)
        self.player_body_pos.append(self.player_head_pos.copy())

    def erase_player(self):
        player_tail_pos = self.player_body_pos[0]
        length_difference = self.player_length - len(self.player_body_pos)
        if length_difference <= 0:
            self.renderer.fill((player_tail_pos[0]), (player_tail_pos[1]), 1, 1, field_color)
            self.player_body_pos.pop(0)
        elif length_difference > 0:
            pass

    def find_new_berry(self):
        possible_positions = [[]]
        for x in range(self.renderer.screen.size_x):
            for y in range(self.renderer.screen.size_y):
                if not [x, y] in self.player_body_pos:
                    possible_positions.append((x, y))
        possible_positions.pop(0)
        if len(possible_positions) == 0:
            # player is in every pixel
            self.won_screen()
            pass
        else:
            picked_position = int(random()*len(possible_positions))
            self.berry_pos = [possible_positions[picked_position][0], possible_positions[picked_position][1]]
            self.renderer.fill((self.berry_pos[0]), (self.berry_pos[1]), 1, 1, berry_color)

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
        smaller_window_side = self.renderer.screen.size_x if self.renderer.screen.size_x <= self.renderer.screen.size_y else self.renderer.screen.size_y
        ray_y = lambda h: (h*self.renderer.screen.size_y/smaller_window_side)  # * 1 + self.start_pos[1]
        for i in range(smaller_window_side):
            self.renderer.fill(i, ray_y(i), 1, 1, (255, 0, 0))
            self.renderer.fill((self.renderer.screen.size_x-1-i), ray_y(i), 1, 1, (255, 0, 0))
        self.update_screen()
        self.restart()

    def collision_detection_self(self):
        if self.player_head_pos in self.player_body_pos:
            return True
        else:
            return False

    def move(self, button: int):
        if button == Controller.BTN_UP:
            if self.player_head_pos[1] > 0:
                self.erase_player()
                self.player_head_pos[1] -= 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else:  # must be outside the borders
                self.game_over()
        elif button == Controller.BTN_DOWN:
            if self.player_head_pos[1] + 1 < self.renderer.screen.size_y:
                self.erase_player()
                self.player_head_pos[1] += 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else:  # must be outside the borders
                self.game_over()
        elif button == Controller.BTN_LEFT:
            if self.player_head_pos[0] > 0:
                self.erase_player()
                self.player_head_pos[0] -= 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else:  # must be outside the borders
                self.game_over()
        elif button == Controller.BTN_RIGHT:
            if self.player_head_pos[0] + 1 < self.renderer.screen.size_x:
                self.erase_player()
                self.player_head_pos[0] += 1
                if self.collision_detection_self():
                    self.game_over()
                self.draw_player()
            else:  # must be outside the borders
                self.game_over()
        self.berry_mechanics()
        self.update_screen()

    def get_time_constant(self):
        return .1
    # wie schnell update ausgefürd werden soll

    def on_player_input(self, player: Player, button: int, status: bool):
        if status:
            self.pressed_button = button
        pass
        # get executed when the player presses a button

    def update(self):
        self.move(self.pressed_button)
        pass
        # get executed every frame
        # game loop

from config import Colors, ControllerBitShifts
from games.GameBase import GameBase
from core.util.Player import Player
from core.util.Vector2 import Vector2
from GameController import GameController
from core.rendering.renderer.RendererBase import RendererBase

# Size of the cursor
PLAYER_SIZE = 3

# Color schema
COLOR_P1 = Colors.BLUE
COLOR_P2 = Colors.RED
COLOR_BALL = Colors.GREEN

# Distance from both edges
DIST_EDGE_Y = 2


# Returns the color of the given player
def get_plr_color(p_id: int):
    return COLOR_P1 if p_id == 0 else COLOR_P2


class Pong(GameBase):
    # Position and motion of the ball
    ball: Vector2
    ball_motion: Vector2 = Vector2(1, 1)

    # Players x and y positions. First index for the first player, second for the second
    player_y: [int, int]
    player_x: [int, int]

    def get_time_constant(self):
        return .1

    # Returns if a given player is colliding with a given position
    def is_plr_colliding(self, p_id: int, x: float, y: float):
        return y == self.player_y[p_id] and self.player_x[p_id] <= x <= self.player_x[p_id] + PLAYER_SIZE+1

    # Returns if the ball is colliding with any player
    def is_ball_colliding_with_player(self, p_id: int):
        return self.is_plr_colliding(p_id, self.ball.x, self.ball.y)

    # Method to update the balls position and collisions
    # Additionally this redraws the ball but doesn't push the leds
    def update_ball(self):
        # Calculates the next ball position
        np_x: float = self.ball.x + self.ball_motion.x
        np_y: float = self.ball.y + self.ball_motion.y

        # Removes the ball from the current position
        clr = COLOR_P1 if self.is_ball_colliding_with_player(0) else COLOR_P2 if self.is_ball_colliding_with_player(
            1) else Colors.OFF
        self.renderer.set_led(int(self.ball.x), int(self.ball.y), clr)

        # Checks if any players might be colliding with the ball
        # and if so, reverts the ball
        for i in range(2):
            if self.is_plr_colliding(i, np_x, np_y):
                self.ball_motion.y = - self.ball_motion.y
                self.update_ball()
                return

        # Checks if the walls are colliding (x)
        if np_x >= self.renderer.screen.size_x or np_x < 0:
            self.ball_motion.x = - self.ball_motion.x
        else:
            self.ball.x = np_x

        # Checks if the walls are colliding (y)
        if np_y >= self.renderer.screen.size_y or np_y < 0:
            self.ball_motion.y = - self.ball_motion.y
        else:
            self.ball.y = np_y

        self.renderer.set_led(int(self.ball.x), int(self.ball.y), COLOR_BALL)

    def on_player_input(self, player: Player, button: int, status: bool):
        # Gets player id
        i = player.get_id()

        # Only acts on upper button flag
        if not status:
            return

        # Checks if a move got pressed
        if button in [Controller.BTN_RIGHT, Controller.BTN_LEFT]:
            # Calculates next x position of the player
            nx = self.player_x[i] + (-1 if button == Controller.BTN_LEFT else 1)

            # Checks if that position is off-screen
            if nx <= 0 or nx + PLAYER_SIZE >= self.renderer.screen.size_x:
                return

            # Gets the pixel that must be removed and the one that must be redrawn
            pxl_to_erase = nx + PLAYER_SIZE + 1 if button == Controller.BTN_LEFT else nx - 1
            pxl_to_draw = nx if button == Controller.BTN_LEFT else nx + PLAYER_SIZE

            # Updates the pixels
            self.renderer.set_led(pxl_to_erase, self.player_y[i], Colors.OFF)
            self.renderer.set_led(pxl_to_draw, self.player_y[i], get_plr_color(i))
            self.renderer.push_leds()

            # Updates player position
            self.player_x[i] = nx

    def init(self, game_controller: GameController, renderer: RendererBase, player_one: Player, player_two: Player):
        super().init(game_controller, renderer, player_one, player_two)

        # Calculates and set init positions of all object
        self.ball = Vector2(self.renderer.screen.size_x / 2, self.renderer.screen.size_y / 2)
        self.player_y = [DIST_EDGE_Y, self.renderer.screen.size_y - DIST_EDGE_Y]
        pos_x = int(self.renderer.screen.size_x / 2 - PLAYER_SIZE / 2)
        self.player_x = [pos_x, pos_x]

        # Renders both players fully for the first time
        for i in range(2):
            self.renderer.fill(self.player_x[i], int(self.player_y[i]), PLAYER_SIZE + 1, 1, get_plr_color(i))
        self.renderer.push_leds()

    def update(self):
        self.update_ball()
        self.renderer.push_leds()

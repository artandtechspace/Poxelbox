from config import Colors
from games.GameBase import GameBase
from core.util.Player import Player
from core.GameController import GameController
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerBitShifts as Controller
import random
from numpy import array


class Test(GameBase):
    relatives: [[int, int]]

    def init(self, game_controller: GameController, renderer: RendererBase, player_one: Player, player_two: Player):
        super().init(game_controller, renderer, player_one, player_two)

        self.relatives = [
            [-1,  0],
            [ 0,  0],
            [ 0, -1],
            [ 1,  0]
        ]

    def render(self):
        self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, (0, 0, 0))

        mid_x = self.renderer.screen.size_x/2
        mid_y = self.renderer.screen.size_y/2

        for cord in self.relatives:
            self.renderer.set_led(mid_x+cord[0], mid_y+cord[1], (255, 0, 255))

        self.renderer.push_leds()

    def get_time_constant(self):
        return .8

    def flip_axes(self):
        for y in range(len(self.relatives)):
            t_coordinate = self.relatives[y][1]
            self.relatives[y][1] = self.relatives[y][0]
            self.relatives[y][0] = t_coordinate

    def invert_axes(self, axis):
        for x in range(len(self.relatives)):
                self.relatives[x][axis] = -self.relatives[x][axis]

    def update(self):
        self.flip_axes()
        self.invert_axes(1)

        print(self.relatives)

        self.render()

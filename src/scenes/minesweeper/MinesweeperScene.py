from random import random

from config import ControllerKeys as Controller
from core.rendering.animations.AnimatedCluster import AnimatedCluster
from core.rendering.renderer.RendererBase import RendererBase
from core.scenery.GameScene import GameScene
from core.scenery.SceneController import SceneController
from core.util.Player import Player
from core.util.Vector2D import Vector2D
from scenes.GameEndScene import GameEndScene

"""
plain tile, Number of adjacent bombs, Flag, Bomb
"""
PLAIN_TILE = (209, 190, 168)  # tan for plain tile
BOMB_TILE = (96, 125, 139)  # metalic petrol for Bombs
FLAG_TILE = (130, 119, 23)  # Olive green for Flag
NO_ADJACENT_BOMBS_TILES = (  # number of adjacent bombs
    (227, 52, 47),  # 0
    (246, 153, 63),  # 1
    (255, 237, 74),  # 2
    (56, 193, 114),  # 3
    (77, 192, 181),  # 4
    (52, 144, 220),  # 5
    (101, 116, 205),  # 6
    (149, 97, 226),  # 7
    (246, 109, 155))  # 8

BORDER_COLOR = (0, 0, 0)  # Black

# all colors for the fade animation
COURSER_COLORS = [(29, 185, 154), (35, 187, 157), (41, 189, 159), (46, 190, 162), (52, 192, 164), (58, 194, 167),
                  (64, 196, 170), (70, 198, 172), (75, 199, 175), (81, 201, 177), (87, 203, 180), (93, 205, 182),
                  (99, 207, 185), (104, 208, 188), (110, 210, 190), (116, 212, 193), (122, 214, 195), (128, 216, 198),
                  (133, 217, 201), (139, 219, 203), (145, 221, 206), (151, 223, 208), (156, 224, 211), (162, 226, 214),
                  (168, 228, 216), (174, 230, 219), (180, 232, 221), (185, 233, 224), (191, 235, 227), (197, 237, 229),
                  (203, 239, 232), (209, 241, 234), (214, 242, 237), (220, 244, 239), (226, 246, 242), (232, 248, 245),
                  (238, 250, 247), (243, 251, 250), (249, 253, 252), (255, 255, 255), (249, 253, 252), (243, 251, 250),
                  (238, 250, 247), (232, 248, 245), (226, 246, 242), (220, 244, 239), (214, 242, 237), (209, 241, 234),
                  (203, 239, 232), (197, 237, 229), (191, 235, 227), (185, 233, 224), (180, 232, 221), (174, 230, 219),
                  (168, 228, 216), (162, 226, 214), (156, 224, 211), (151, 223, 208), (145, 221, 206), (139, 219, 203),
                  (133, 217, 201), (128, 216, 198), (122, 214, 195), (116, 212, 193), (110, 210, 190), (104, 208, 188),
                  (99, 207, 185), (93, 205, 182), (87, 203, 180), (81, 201, 177), (75, 199, 175), (70, 198, 172),
                  (64, 196, 170), (58, 194, 167), (52, 192, 164), (46, 190, 162), (41, 189, 159),
                  (35, 187, 157)]  # light blue
# relative coordinates for courser
COURSER_SECTION = [Vector2D(4, 0), Vector2D(3, 0), Vector2D(-4, 0), Vector2D(-3, 0), Vector2D(0, 4), Vector2D(0, 3),
                   Vector2D(0, -4), Vector2D(0, -3)]


class Tile:
    """
    Tiles:
            Plain tile; default status
            Hidden:
                Bomb
            Shown:
                number of adjacent bombs (0 to 8)
                Flag
                exploding bomb
    """
    visible = False
    is_bomb = False
    is_flagged = False
    no_adjacent_bombs: int

    def get_color(self):
        """
        returns the color of this tile
        """
        if self.is_flagged:
            return FLAG_TILE
        elif not self.visible:
            return PLAIN_TILE
        elif self.is_bomb:
            return BOMB_TILE
        elif hasattr(self, 'no_adjacent_bombs'):
            return NO_ADJACENT_BOMBS_TILES[self.no_adjacent_bombs]
        else:
            raise Exception('Invalid')


class MinesweeperScene(GameScene):
    screen_middle: Vector2D
    player_position: Vector2D

    plane_size = Vector2D(10, 10)
    field: [[Tile]]

    is_first_move: bool
    no_bombs: int
    bomb_tolerance: float

    courser: AnimatedCluster

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)

        # initialise variables
        self.player_position = Vector2D(int(self.plane_size.x / 2), int(self.plane_size.y / 2))
        self.field = [[Tile() for y in range(self.plane_size.y)] for x in range(self.plane_size.x)]
        self.screen_middle = Vector2D(int(self.renderer.screen.size_x / 2), int(self.renderer.screen.size_y / 2))
        self.render_screen()
        self.courser = AnimatedCluster(self.screen_middle, COURSER_COLORS, COURSER_SECTION)

        # adds randomness to the number of bombs
        self.is_first_move = True
        self.no_bombs = int((self.plane_size.x * self.plane_size.y) * 0.25)
        self.bomb_tolerance = (self.plane_size.x * self.plane_size.y) * 0.1
        self.no_bombs += int((random() - .5) * self.bomb_tolerance)

    def get_time_constant(self):
        return 0.01

    def on_player_input(self, player: Player, button: int, status: bool):
        # Handles the loading screen
        if super().on_handle_loading_screen(button, status):
            return

        """
        Controls:
        UP    = move up
        DOWN  = move down
        LEFT  = move left
        Right = move right
        A     = uncover tile
        B     = place flag
        """

        # only acts when a button is pressed
        if not status:
            return

        # courser movement in y direction
        if button in (Controller.BTN_UP, Controller.BTN_DOWN):
            self.player_position.y += 1 if button == Controller.BTN_UP else -1
            self.render_screen()
            return

        # courser movement in x direction
        if button in (Controller.BTN_LEFT, Controller.BTN_RIGHT):
            self.player_position.x += 1 if button == Controller.BTN_RIGHT else -1
            self.render_screen()
            return

        # aborts if the player is outside the field
        if self.player_position.x not in range(self.plane_size.x) or \
                self.player_position.y not in range(self.plane_size.y):
            return

        # uncover tile
        if button == Controller.BTN_A:

            # if it's the first move, place bombs
            if self.is_first_move:
                self.place_bombs(self.player_position)
                self.is_first_move = False

            # if the current tile is a bomb -> GameOver
            if self.field[self.player_position.x][self.player_position.y].is_bomb:
                for idx_x in range(self.plane_size.x):
                    for idx_y in range(self.plane_size.y):
                        self.place_nu_adjacent(Vector2D(idx_x, idx_y))

                # loads game end scene
                self.render_screen()
                game_end = GameEndScene()
                game_end.reload_scene = self
                self.scene_controller.load_scene(game_end)
                return

            # Display number of adjacent bombs
            self.place_nu_adjacent(self.player_position)

            # showing nearby tiles when the tile is a zero
            if self.field[self.player_position.x][self.player_position.y].no_adjacent_bombs == 0:
                positions = []
                zero_positions = [self.player_position]

                # gets nearby tiles of the fist shown zero tile
                for row in range(-1, 2, 1):
                    for y in range(-1, 2, 1):
                        t_vector = self.player_position + Vector2D(row, y)

                        # excludes known zero tiles and position outside the plane
                        if t_vector.x in range(0, self.plane_size.x) and \
                                t_vector.y in range(0, self.plane_size.y) and \
                                t_vector != self.player_position:
                            positions.append(t_vector)

                for pos in positions:
                    # shows nearby tiles of the shown zero tiles
                    self.place_nu_adjacent(pos)

                    # adds neighbours of nearby tiles which are also a zero
                    if self.field[pos.x][pos.y].no_adjacent_bombs == 0:
                        zero_positions.append(pos)
                        for row in range(-1, 2, 1):
                            for y in range(-1, 2, 1):
                                t_vector = pos + Vector2D(row, y)

                                # excludes known zero tiles and position outside the plane
                                if t_vector.x in range(0, self.plane_size.x) and \
                                        t_vector.y in range(0, self.plane_size.y) and \
                                        t_vector not in zero_positions:
                                    positions.append(t_vector)

        # flagg tile
        if button == Controller.BTN_B and not self.field[self.player_position.x][self.player_position.y].visible:
            # toggles flagged status
            self.field[self.player_position.x][self.player_position.y].is_flagged = \
                not self.field[self.player_position.x][self.player_position.y].is_flagged

            # checks if the player flagged the last bomb
            won = not self.is_first_move
            for row in self.field:
                for pos in row:
                    won = won and (pos.is_flagged == pos.is_bomb)
            # loads end game scene
            if won:
                game_end = GameEndScene()
                game_end.reload_scene = self
                game_end.won_game = True
                self.scene_controller.load_scene(game_end)
                return

        self.render_screen()

    def on_update(self):
        # draws courser
        self.courser.position = self.screen_middle
        self.courser.render(self.renderer)

        self.renderer.push_leds()

    def render_screen(self):
        # for every pixel on the screen
        for x in range(self.renderer.screen.size_x):
            for y in range(self.renderer.screen.size_y):

                # maps screen coordinates to field coordinates
                x_pos = int(x + self.player_position.x - self.screen_middle.x)
                y_pos = int(y + self.player_position.y - self.screen_middle.y)

                # Draws the tile's color if the calculated field coordinates are truly within the field
                if x_pos in range(0, self.plane_size[0]) and y_pos in range(0, self.plane_size[1]):
                    self.renderer.set_led(int(x), int(y), self.field[x_pos][y_pos].get_color())

                # must be outside the field
                else:
                    self.renderer.set_led(int(x), int(y), BORDER_COLOR)

        self.renderer.push_leds()

    def place_nu_adjacent(self, position: Vector2D):
        # Display number of adjacent bombs
        sum_bombs = 0
        for dx in range(-1, 2, 1):
            for dy in range(-1, 2, 1):

                # skips if the position to check is still within the boundaries of the field
                if position.x + dx not in range(0, self.plane_size.x) or \
                        position.y + dy not in range(0, self.plane_size.y):
                    continue

                # if an adjacent tile is a bomb, increment sum bombs
                if self.field[position.x + dx][position.y + dy].is_bomb:
                    sum_bombs += 1

        # gives sum of bombs to tile
        self.field[position.x][position.y].no_adjacent_bombs = sum_bombs
        self.field[position.x][position.y].visible = True

    def place_bombs(self, exclude_pos: Vector2D):
        # places bombes
        while self.no_bombs > 0:
            pos_x = int(random() * self.plane_size.x)
            pos_y = int(random() * self.plane_size.y)

            # if the random position is not the exclude_pos, place bomb
            if pos_x != exclude_pos.x and pos_y != exclude_pos.y:
                self.field[pos_x][pos_y].is_bomb = True
                self.no_bombs -= 1

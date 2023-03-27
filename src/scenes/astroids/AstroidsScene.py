import time
from math import sin, cos

from core.scenery.GameScene import GameScene
from core.util.Player import Player
from core.scenery.SceneController import SceneController
from core.rendering.renderer.RendererBase import RendererBase
from config import ControllerKeys as Keys
from core.util.Vector2D import Vector2D
from scenes.GameEndScene import GameEndScene

astroids_per_wave = (5, 3)
ASTROID_COLOR   = (211,   211,    211)    # light gray
BULLET_COLOR    = (50,    220,    170)    # blue-green
SPACE_COLOR     = (0,     0,      0)      # black

BULLET_SPEED = 0.5
ASTROID_SPEED = 0.2


class Particle:
    pos: Vector2D
    mov: Vector2D

    def __init__(self, position, movement):
        self.pos = position
        self.mov = movement


class AstroidsScene(GameScene):
    astroids: list[Particle]
    bullets: list[Particle]
    player_pos: Vector2D
    player_dir: float
    last_exec_ast: float
    last_exec_bul: float

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)

    def get_time_constant(self):
        return 0.05

    def on_player_input(self, player: Player, button: int, status: bool):
        # Handles the loading screen
        if super().on_handle_loading_screen(button, status):
            return

        if status:
            if button == Keys.BTN_A:
                # shoot
                self.bullets.append(Particle(self.player_pos, Vector2D(cos(self.player_dir), sin(self.player_dir))))
            if button == Keys.ARROW_KEYS:
                pass  # TODO: how to aim?

    def on_update(self):
        clc_time = time.perf_counter()

        if self.last_exec_ast - clc_time <= 0:
            self.last_exec_ast = clc_time + ASTROID_SPEED

            self.astroid_movement()

        if self.last_exec_bul - clc_time <= 0:
            self.last_exec_bul = clc_time + BULLET_SPEED

            self.bullet_movement()

    def astroid_movement(self):
        for ast in self.astroids:

            self.renderer.set_led_vector(ast.pos, SPACE_COLOR)
            ast.pos += ast.mov

            # check for screen boundaries
            if ast.pos.x >= self.renderer.screen.size_x:
                ast.pos.x = 0
            elif ast.pos.x <= 0:
                ast.pos.x = self.renderer.screen.size_x - 1
            if ast.pos.y >= self.renderer.screen.size_y:
                ast.pos.y = 0
            elif ast.pos.y <= 0:
                ast.pos.y = self.renderer.screen.size_y - 1

            self.renderer.set_led_vector(ast.pos, ASTROID_COLOR)

            # collision detection
            for bul in self.bullets:
                self.collision_detection(ast, bul)

    def bullet_movement(self):
        for bul in self.bullets:

            self.renderer.set_led_vector(bul.pos, SPACE_COLOR)
            bul.pos += bul.mov

            # check for screen boundaries
            if bul.pos.x >= self.renderer.screen.size_x or bul.pos.x <= 0 or \
                    bul.pos.y >= self.renderer.screen.size_y or bul.pos.y <= 0:
                self.bullets.remove(bul)

            self.renderer.set_led_vector(bul.pos, BULLET_COLOR)

            # collision detection
            for ast in self.astroids:
                self.collision_detection(ast, bul)

    def collision_detection(self, t_ast: Particle, t_bul: Particle):
        if t_ast.pos == t_bul.pos:
            self.bullets.remove(t_bul)
            self.astroids.remove(t_ast)
            self.renderer.set_led_vector(t_ast.pos, SPACE_COLOR)

    def won_screen(self):
        game_end = GameEndScene()
        game_end.reload_scene = self
        game_end.won_game = True
        self.scene_controller.load_scene(game_end)

    def game_over(self):
        game_end = GameEndScene()
        game_end.reload_scene = self
        self.scene_controller.load_scene(game_end)

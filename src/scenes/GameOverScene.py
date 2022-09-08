from config import Colors
from core.rendering.renderer.RendererBase import RendererBase
from core.scenery.SceneBase import SceneBase
from core.util.Player import Player
from core.scenery.SceneController import SceneController


class GameOverScene(SceneBase):
    reload_scene: any

    def on_init(self, scene_controller: SceneController, renderer: RendererBase, player_one: Player,
                player_two: Player):
        super().on_init(scene_controller, renderer, player_one, player_two)
        self.scene_controller = scene_controller

        self.renderer.fill(0, 0, renderer.screen.size_x, renderer.screen.size_y, Colors.OFF)

        thickness = 1
        def ray(x: int): return int(x * self.renderer.screen.size_y / self.renderer.screen.size_x)
        if self.renderer.screen.size_y % 2 == 0 or self.renderer.screen.size_x % 2 == 0:
            def ray(x: int): return int(x * (self.renderer.screen.size_y + 1) / self.renderer.screen.size_x)
            thickness += 1
        for i in range(self.renderer.screen.size_x):
            for j in range(thickness):
                j = j - int(thickness/2)
                self.renderer.set_led(i, ray(i) + j, Colors.RED)
                self.renderer.set_led(i, self.renderer.screen.size_y - 1 - j - ray(i), Colors.RED)
        self.renderer.push_leds()

    def get_time_constant(self):
        return .1

    def on_update(self):
        pass

    def on_player_input(self, player: Player, button: int, status: bool):
        if status:
            self.renderer.fill(0, 0, self.renderer.screen.size_x, self.renderer.screen.size_y, Colors.OFF)
            self.scene_controller.load_scene(self.reload_scene)

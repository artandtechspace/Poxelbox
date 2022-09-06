import time
from core.util.Player import Player
from core.rendering.renderer.RendererBase import RendererBase
from core.userinput.BaseUserInput import BaseUserInput
import config.ControllerKeys as Keys
import config.Config as Cfg


class SceneController:
    # Players that are interacting with the scene
    players: (Player, Player) = (Player(), Player())

    # Renderer used for the scene
    rdr: RendererBase

    # Selected scene
    scene: any  # NOTE: Declaired as any to avoid circular import
    loading_scene: any

    # User-input method
    userinp: BaseUserInput

    def __init__(self, renderer: RendererBase, userinput: BaseUserInput, p_loading_scene: any):
        self.loading_scene = p_loading_scene
        self.rdr = renderer
        self.userinp = userinput

    # shows the loading screen
    def load_loading_scene(self):
        self.scene = self.loading_scene
        self.loading_scene.reload()

    # Used to open a new scene
    def load_scene(self, next_scene: any):
        self.scene = next_scene

        # Init's the game
        self.scene.on_init(self, self.rdr, self.players[0], self.players[1])

    # Executes when any users control's change
    def __on_raw_player_input(self, status: int):
        # Gets the player
        plr = status & 1
        self.players[plr].update_status(status >> 1)

    # Executes when the player triggers a button or releases a button
    def __on_player_input(self, player, button, status):
        # Enters the loading screen
        if status and button == Keys.BTN_SELECT:
            self.load_loading_scene()
        else:
            self.scene.on_player_input(player, button, status)

    # Must be executed before the run-method is executed. Prepares the pi for rendering and other stuff
    def prepare(self):
        # Init's all stuff
        self.players[0].init(0, self.__on_player_input)
        self.players[1].init(1, self.__on_player_input)
        self.userinp.start(self.__on_raw_player_input)

        # Init's the loading screen
        self.loading_scene.on_init(self, self.rdr, self.players[0], self.players[1])

    # Starts the scene-loop and execution
    def run(self):
        # When the scene-loop executed last
        last_exec = time.perf_counter() + self.scene.get_time_constant() / Cfg.APP_SPEED

        # Game loop
        while True:
            # Updates the controller input-handler
            self.userinp.update()

            # Gets the current time in relation
            clc_time = time.perf_counter()
            # Updates the frame on time
            if last_exec - clc_time <= 0:
                # Updates the time before any rendering is done
                last_exec = clc_time + self.scene.get_time_constant() / Cfg.APP_SPEED
                # Executes the scene loop
                self.scene.on_update()

            time.sleep(0.05)

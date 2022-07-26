import time
from core.util.Player import Player
from core.rendering.renderer.RendererBase import RendererBase
from core.userinput.BaseUserInput import BaseUserInput
from config.Config import Scene_SPEED as TIME_MULTIPLIER

class SceneController:
    # Players that are interacting with the scene
    players: (Player, Player) = (Player(), Player())

    # Renderer used for the scene
    rdr: RendererBase

    # Selected scene
    scene: any               # TODO: Declaired as any to avoid circular import

    # User-input method
    userinp: BaseUserInput

    def __init__(self, renderer: RendererBase, userinput: BaseUserInput):
        self.rdr = renderer
        self.userinp = userinput

    # Used to open a new scene
    def load_game(self, next_scene):
        self.scene = next_scene

        # Init's the game
        self.scene.init(self, self.rdr, self.players[0], self.players[1])

    # Executes when any users control's change
    def __on_raw_player_input(self, status: int):
        # Gets the player
        plr = status & 1
        self.players[plr].update_status(status >> 1)

    # Executes when the player triggers a button or releases a button
    def __on_player_input(self, player, button, status):
        self.scene.on_player_input(player, button, status)

    # Must be executed before the run-method is executed. Prepares the pi for rendering and other stuff
    def prepare(self):
        # Init's all stuff
        self.players[0].init(0, self.__on_player_input)
        self.players[1].init(1, self.__on_player_input)
        self.userinp.start(self.__on_raw_player_input)

        # Resets the grid
        self.rdr.fill(0, 0, self.rdr.screen.size_x, self.rdr.screen.size_y, (0, 0, 0))
        self.rdr.push_leds()

    # Starts the scene-loop and execution
    def run(self):
        # When the scene-loop executed last
        last_exec = time.perf_counter() + self.scene.get_time_constant() / TIME_MULTIPLIER

        # Game loop
        while True:
            # Updates the controller input-handler
            self.userinp.update()

            # Gets the current time in relation
            clc_time = time.perf_counter()
            # Updates the frame on time
            if last_exec - clc_time <= 0:
                # Updates the time before any rendering is done
                last_exec = clc_time + self.scene.get_time_constant() / TIME_MULTIPLIER
                # Executes the scene loop
                self.scene.update()

            time.sleep(0.05)

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

    # Time when the next update shall be send to the scene
    last_exec: int = 0

    def __init__(self, renderer: RendererBase, userinput: BaseUserInput):
        self.rdr = renderer
        self.userinp = userinput

    # Used to open a new scene
    def load_scene(self, next_scene: any):
        self.scene = next_scene

        # Unit's the game
        try:
            self.scene.on_init(self, self.rdr, self.players[0], self.players[1])
        except Exception as e:
            import traceback
            print(e)
            traceback.print_exc()
            
            self.__on_scene_crash()
            return

    # Execute whenever a scene crashes do to some error
    def __on_scene_crash(self):
        # Sends the player to the crash-scene
        from scenes.CrashedScreenScene import CrashedScreenScene
        self.load_scene(CrashedScreenScene())

    # Executes when any users control's change
    def __on_raw_player_input(self, status: int):
        # Gets the player
        plr = status & 1
        self.players[plr].update_status(status >> 1)

    # Executes when the player triggers a button or releases a button
    def __on_player_input(self, player, button, status):
        # Executes the scene loop
        try:
            self.scene.on_player_input(player, button, status)
        except Exception as e:
            print(e)
            self.__on_scene_crash()
            return

    # Must be executed before the run-method is executed. Prepares the pi for rendering and other stuff
    def prepare(self):
        # Init's all stuff
        self.players[0].init(0, self.__on_player_input)
        self.players[1].init(1, self.__on_player_input)
        self.userinp.start(self.__on_raw_player_input)

    # Starts the scene-loop and execution
    def update(self):
        # Updates the controller input-handler
        self.userinp.update()

        # Gets the current time in relation
        clc_time = time.perf_counter()
        # Updates the frame on time
        if self.last_exec - clc_time <= 0:
            # Updates the time before any rendering is done
            self.last_exec = clc_time + self.scene.get_time_constant()
            # Executes the scene loop
            try:
                self.scene.on_update()
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                self.__on_scene_crash()
                return

        time.sleep(0.05)

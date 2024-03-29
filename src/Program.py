import json
import multiprocessing
import sys
import time
from multiprocessing import Process
from os.path import exists

import ProgramInfo as __ProgInfo
import config.Config as Cfg
import config.ConfigSettings as __CfgSettings
import config.core.ConfigLoader as __CfgLoader
import core.scenery.SceneController as __SceneController
import webendpoints.Webserver as __Webserver
from core.scenery.PiTestScene import PiTestScene
from scenes import LoadingScreenScene

# Scene-manager
scene_manager: __SceneController.SceneController

# Config-loader
config_loader: __CfgLoader.ConfigLoader

# Process of the webserver
__web_server_ps: Process

# Thread-safe variable to check if the program is terminated
is_terminated = multiprocessing.Manager().Value(bool, False)
# Thread-safe variable to check if the program should be terminated when the
# game-logic is inside the selection-screen
should_terminate_in_future = multiprocessing.Manager().Value(bool, False)


# Queues the program to be stopped
def stop():
    global is_terminated
    is_terminated.set(True)


# Queues the program to stop when the game-logic dems the appropriate
def preload_stop():
    global should_terminate_in_future
    should_terminate_in_future.set(True)


# Kills the program and all subthreads
# Requires execution from main thread
def kill_program():
    global __web_server_ps

    # Kills pygame if it exists
    try:
        import pygame
        pygame.quit()
    except:
        pass

    # Kills webserver if it exists
    try:
        __web_server_ps.kill()
    except:
        pass

    # Kills program
    sys.exit()


# Starts the program with the given parameters
def initalize():
    global scene_manager, config_loader, __web_server_ps
    # Registers the config-loaders
    config_loader = __CfgSettings.register_on_loader()

    # Loads the config (If it exists)
    if exists(__ProgInfo.CONFIG_PATH):
        with open(__ProgInfo.CONFIG_PATH, mode='r') as fp:
            try:
                # Tries to from the json inside the file
                config_loader.try_load_from_json(json.loads(fp.read()))
            except:
                pass

    with open(__ProgInfo.CONFIG_PATH, mode='w') as fp:
        # Exports, writes and updates the file
        fp.write(config_loader.export_to_json())

    renderer = None
    input_method = None
    scene = None

    # Checks the selected environment

    # Development-env
    if Cfg.IS_DEVELOPMENT_ENVIRONMENT:
        from core.rendering.renderer.PyGameRenderer import PyGameRenderer
        from core.userinput.PyGameUserInput import PyGameUserInput

        renderer = PyGameRenderer()
        input_method = PyGameUserInput()
    # Pi-env
    else:
        from core.rendering.renderer.WS2812BRenderer import WS2812BRenderer
        from core.userinput.SerialEspUserInput import SerialEspUserInput

        renderer = WS2812BRenderer()
        input_method = SerialEspUserInput()

    # Gets the first scene
    if Cfg.USE_TEST_SCENE:
        scene = PiTestScene()
    else:
        # Initializes the load-screen
        LoadingScreenScene.init_loading_screen()
        scene = LoadingScreenScene.LoadingScreenScene()

    if sys.platform != 'win32':
        # Starts the webserver
        __web_server_ps = __Webserver.start()

    # Creates game controller, prepares it and loads the scene
    scene_manager = __SceneController.SceneController(renderer, input_method)

    renderer.setup()

    scene_manager.prepare()
    scene_manager.load_scene(scene)

    game_loop()


def game_loop():
    global is_terminated
    while True:
        if is_terminated.get():
            time.sleep(0.2)
            kill_program()

        scene_manager.update()

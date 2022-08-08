import config.core.ConfigLoader as __CfgLoader
import core.scenery.SceneController as __SceneController
import webendpoints.Webserver as __Webserver
import config.ConfigSettings as __CfgSettings
import ProgramInfo as __ProgInfo
import core.scenery.SceneBase as __SceneBase
import core.userinput.BaseUserInput as __BaseUserInput
import core.rendering.renderer.RendererBase as __RendererBase
from multiprocessing import Process
import sys
import json

# Scene-manager
scene_manager: __SceneController.SceneController

# Config-loader
config_loader: __CfgLoader.ConfigLoader

# Process of the webserver
__web_server_ps: Process

# Stops the program and kills it
def stop():
    global __web_server_ps

    __web_server_ps.kill()
    sys.exit()


# Starts the program with the given parameters
def initalize(renderer: __RendererBase.RendererBase, userinput: __BaseUserInput.BaseUserInput,
              scene: __SceneBase.SceneBase):
    global scene_manager, config_loader, __web_server_ps
    # Registers the config-loaders
    config_loader = __CfgSettings.register_on_loader()

    # Loads the config
    with open(__ProgInfo.CONFIG_PATH, mode='r') as fp:
        try:
            # Tries to from the json inside the file
            config_loader.try_load_from_json(json.loads(fp.read()))
        except:
            pass

    with open(__ProgInfo.CONFIG_PATH, mode='w') as fp:
        # Exports, writes and updates the file
        fp.write(config_loader.export_to_json())

    # Starts the webserver
    __web_server_ps = __Webserver.start()

    # Creates game controller, prepares it and loads the scene
    scene_manager = __SceneController.SceneController(renderer, userinput)

    renderer.setup()

    scene_manager.prepare()
    scene_manager.load_scene(scene)
    scene_manager.run()

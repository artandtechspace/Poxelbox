import config.Config
from core.scenery.SceneController import SceneController
from config.ConfigSettings import register_on_loader as register_config_loader

# Config-location
CONFIG_LOCATION = "rsc/config.json"


def start(renderer, userinput, game):
    # Registers the config-loaders
    cfgloader = register_config_loader()

    # Loads the config
    with open(CONFIG_LOCATION, mode='r') as fp:
        # Tries to from the json inside the file
        cfgloader.try_load_from_json(fp.read())

    with open(CONFIG_LOCATION, mode='w') as fp:
        # Exports, writes and updates the file
        fp.write(cfgloader.export_to_json())

    print(config.Config.APP_SPEED)

    # Creates game controller, prepares it and loads the game
    ctrl = SceneController(renderer, userinput)

    renderer.setup()

    ctrl.prepare()
    ctrl.load_game(game)
    ctrl.run()

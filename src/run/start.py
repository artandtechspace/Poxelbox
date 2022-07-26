from core.scenery.SceneController import SceneController

def start(renderer, userinput, game):
    # Creates game controller, prepares it and loads the game
    ctrl = SceneController(renderer, userinput)

    renderer.setup()

    ctrl.prepare()
    ctrl.load_game(game)
    ctrl.run()

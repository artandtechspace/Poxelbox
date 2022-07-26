from core.GameController import GameController

def start(renderer, userinput, game):
    # Creates game controller, prepares it and loads the game
    ctrl = GameController(renderer, userinput)

    ctrl.prepare()
    ctrl.load_game(game)
    ctrl.run()

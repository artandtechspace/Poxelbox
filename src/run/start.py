from games.pong.Pong import Pong
from core.GameController import GameController

def start(renderer, userinput):
    # Creates game controller, prepares it and loads the game
    ctrl = GameController(renderer, userinput)

    ctrl.prepare()
    ctrl.load_game(Pong())
    ctrl.run()

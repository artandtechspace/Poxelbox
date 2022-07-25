from core.userinput.DummyUserInput import DummyUserInput
from games.pong.Pong import Pong
from GameController import GameController
from core.rendering.renderer.PyGameRenderer import PyGameRenderer
from core.rendering.Screen import Screen

# Selects the renderer and user-input method
renderer = PyGameRenderer(Screen(18, 20))
userinp = DummyUserInput()

# Creates game controller, preapres it and loads the game
ctrl = GameController(renderer, userinp)

ctrl.prepare()
ctrl.load_game(Pong())
ctrl.run()

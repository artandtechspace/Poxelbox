from core.userinput.DummyUserInput import DummyUserInput
from core.rendering.renderer.PyGameRenderer import PyGameRenderer
from core.rendering.Screen import Screen
from run.start import start
from games.snake.SnakeScene import SnakeScene
from games.pong.PongScene import PongScene
import pygame
from core.userinput.PyGameUserInput import PyGameUserInput

# Starts pygame
pygame.init()

start(PyGameRenderer(Screen(18, 20)), PyGameUserInput(), PongScene())
import Program
from core.rendering.renderer.PyGameRenderer import PyGameRenderer
from core.rendering.Screen import Screen
from games.snake.SnakeScene import SnakeScene
from games.pong.PongScene import PongScene
import pygame
from core.userinput.PyGameUserInput import PyGameUserInput

# Starts pygame
pygame.init()

Program.initalize(PyGameRenderer(Screen(18, 20)), PyGameUserInput(), SnakeScene())
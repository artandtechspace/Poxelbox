import Program
from core.rendering.renderer.PyGameRenderer import PyGameRenderer
from games.pong.PongScene import PongScene
from games.tetris.TetrisScene import TetrisScene
import pygame
from core.userinput.PyGameUserInput import PyGameUserInput

def start():
    # Starts pygame
    pygame.init()

    Program.initalize(PyGameRenderer(), PyGameUserInput(), TetrisScene())

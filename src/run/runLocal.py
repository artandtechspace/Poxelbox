import Program
from core.rendering.renderer.PyGameRenderer import PyGameRenderer
from games.pong.PongScene import PongScene
import pygame
from core.userinput.PyGameUserInput import PyGameUserInput

def start():
    # Starts pygame
    pygame.init()

    Program.initalize(PyGameRenderer(), PyGameUserInput(), PongScene())

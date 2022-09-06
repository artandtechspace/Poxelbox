import Program
from core.rendering.renderer.PyGameRenderer import PyGameRenderer
import pygame
from core.userinput.PyGameUserInput import PyGameUserInput
from core.scenery.LoadingScreen import LoadingScreen


def start():
    # Starts pygame
    pygame.init()

    Program.initalize(PyGameRenderer(), PyGameUserInput(), LoadingScreen())

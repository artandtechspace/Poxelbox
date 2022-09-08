import Program
from core.rendering.renderer.PyGameRenderer import PyGameRenderer
import pygame
from core.userinput.PyGameUserInput import PyGameUserInput
from scenes.LoadingScreenScene import LoadingScreenScene


def start():
    # Starts pygame
    pygame.init()

    Program.initalize(PyGameRenderer(), PyGameUserInput(), LoadingScreenScene())

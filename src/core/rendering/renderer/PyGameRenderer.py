from core.rendering.renderer.RendererBase import RendererBase
import sys
import pygame
from config.Config import PyGameRenderer_LED_PIXEL_SCALE as PIXEL


class PyGameRenderer(RendererBase):
    # Window object
    __window = None

    def setup(self):
        # Creates the window object
        self.__window = pygame.display.set_mode((self.screen.size_x * PIXEL, self.screen.size_y * PIXEL))

    def set_led(self, x: int, y: int, color: (int, int, int)):
        # Draws the rect
        pygame.draw.rect(self.__window, color, [x * PIXEL, self.screen.size_y * PIXEL - PIXEL * (y + 1), PIXEL, PIXEL], 0)
        pass

    def push_leds(self):
        pygame.display.update()
        pass

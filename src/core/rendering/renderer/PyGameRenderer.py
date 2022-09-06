from core.rendering.renderer.RendererBase import RendererBase
import pygame
import config.Config as Cfg


class PyGameRenderer(RendererBase):
    # Window object
    __window = None

    def setup(self):
        super().setup()
        # Creates the window object
        self.__window = pygame.display.set_mode((self.screen.size_x * Cfg.LED_PIXEL_SCALE, self.screen.size_y * Cfg.LED_PIXEL_SCALE))

    def set_led(self, x: int, y: int, color: (int, int, int)):
        # Draws the rect
        pygame.draw.rect(self.__window, color, [x * Cfg.LED_PIXEL_SCALE, self.screen.size_y * Cfg.LED_PIXEL_SCALE - Cfg.LED_PIXEL_SCALE * (y + 1), Cfg.LED_PIXEL_SCALE, Cfg.LED_PIXEL_SCALE], 0)
        pass

    def push_leds(self):
        pygame.display.update()
        pass

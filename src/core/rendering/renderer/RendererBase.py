from core.rendering.Screen import Screen


class RendererBase:
    # Screen with some properties
    screen: Screen

    def __init__(self, screen: Screen):
        self.screen = screen

    def setup(self):
        pass

    # Fills the pixels from start to end with the given color (May be overriden with better code inside the specific renderer)
    def fill(self, start_x: int, start_y: int, width: int, height: int, color: (int, int, int)):
        for x in range(width):
            for y in range(height):
                self.set_led(x + start_x, y + start_y, color)
        pass

    def set_led(self, x: int, y: int, color: (int, int, int)):
        pass

    def push_leds(self):
        pass

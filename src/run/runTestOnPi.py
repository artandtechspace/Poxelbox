from core.rendering.renderer.WS2812BRenderer import WS2812BRenderer
from time import sleep


def start():
    renderer = WS2812BRenderer()

    for y in range(renderer.screen.size_y):
        for x in range(renderer.screen.size_x):
            renderer.set_led(x, y, (255, 0, 0))
            sleep(.5)

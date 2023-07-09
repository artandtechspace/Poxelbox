from core.rendering.renderer.BoxSchemaRendererBase import BoxSchemaRendererBase
import board
import neopixel


class WS2812BRenderer(BoxSchemaRendererBase):

    def __init__(self):
        super().__init__()

        # WS2812B-Access class
        self.__pixels: neopixel.NeoPixel = None

    def setup(self):
        super().setup()

        self.__pixels = neopixel.NeoPixel(board.D12, self.screen.size_x * self.screen.size_y, auto_write=False,
                                          pixel_order=neopixel.RGB)

    def set_box_schema_led(self, idx: int, color: (int, int, int)):
        # Sets the given pixel
        self.__pixels[idx] = color

    def push_leds(self):
        self.__pixels.show()

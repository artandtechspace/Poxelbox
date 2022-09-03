from core.rendering.renderer.RendererBase import RendererBase
import board
import neopixel
import config.Config as Cfg


class WS2812BRenderer(RendererBase):
    # WS2812B-Access class
    __pixels: neopixel.NeoPixel

    def setup(self):
        self.__pixels = neopixel.NeoPixel(board.D18, self.screen.size_x * self.screen.size_y, auto_write=False)

    def set_led(self, x: int, y: int, color: (int, int, int)):
        # Sets the given pixel
        self.__pixels[self.__get_pixel_id(x,y)] = color

    def push_leds(self):
        self.__pixels.show()

    '''
    Method that takes in an x and y coordinate, calculates the exact pixel-id on the strip and returns it
    '''
    def __get_pixel_id(self, x: int, y: int):
        # Which box position on the wall this pixel belongs to
        # Pixel x = 7 would mean the 3rd box on the wall
        box_x = x // Cfg.CUBE_SIZE_X
        box_y = y // Cfg.CUBE_SIZE_Y

        # Offset of the pixel from it's base box
        # x = 7 would mean an offset of 1
        offset_from_box_x = x - box_x * Cfg.CUBE_SIZE_X
        offset_from_box_y = y - box_y * Cfg.CUBE_SIZE_Y

        # Calculates the amount of boxes that got skipped by this set of coordinates
        skipped_boxes = box_x * Cfg.WALL_SIZE_Y + (
            # Bottom start
            (
                box_y
            )
            # Checks if the current column started from the bottom or top
            if box_x & 1 == 0 else
            # Top-start
            (
                (Cfg.WALL_SIZE_Y - box_y - 1)
            )
        )

        # Calculates the amount of lines inside the led's box that got skipped
        before_rows_skipped = (
            offset_from_box_y
            if box_x & 1 == 0 else
            (Cfg.CUBE_SIZE_Y - offset_from_box_y - 1)
        )

        # Calculates the amount of leds skipped inside the leds row
        leds_in_row = (
            offset_from_box_x + 1
            if offset_from_box_y & 1 == 0 else
            3 - offset_from_box_x
        )

        # Calcualtes the actual led position and shifts it
        return skipped_boxes * self.screen.size_y * self.screen.size_x + before_rows_skipped * (Cfg.CUBE_SIZE_Y - 1) + leds_in_row - 1

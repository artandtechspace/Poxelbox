from core.rendering.renderer.RendererBase import RendererBase
import board
import neopixel
import config.Config as Cfg

rel_idx = lambda rel_x, rel_y: (rel_y + 4) if rel_x == 2 else \
    12 - rel_y + rel_x * (5 - 2 * rel_y) + int(rel_y < 2) * (-10 - 4 * rel_x)


class WS2812BRenderer(RendererBase):
    # WS2812B-Access class
    __pixels: neopixel.NeoPixel

    __rel_idx__: callable

    def setup(self):
        super().setup()

        global rel_idx

        # TOD0: Allow different orientations for each box

        if "X" == Cfg.BOX_ORIENTATION[1]:   # (X | Y)
            if "Y" == Cfg.BOX_ORIENTATION[5]:
                self.__rel_idx__ = rel_idx
            else:
                self.__rel_idx__ = lambda rel_x, rel_y: rel_idx(rel_x, Cfg.BOX_SIZE_Y-1-rel_y)
        else:                               # (-X | Y)
            if "Y" == Cfg.BOX_ORIENTATION[6]:
                self.__rel_idx__ = lambda rel_x, rel_y: rel_idx(Cfg.BOX_SIZE_X-1-rel_x, rel_y)
            else:
                self.__rel_idx__ = lambda rel_x, rel_y: rel_idx(Cfg.BOX_SIZE_X-1-rel_x, Cfg.BOX_SIZE_Y-1-rel_y)

        self.__pixels = neopixel.NeoPixel(board.D12, self.screen.size_x * self.screen.size_y, auto_write=False, pixel_order=neopixel.RGB)

    def set_led(self, x: int, y: int, color: (int, int, int)):
        # Ensures the position is on screen
        if x >= self.screen.size_x or y >= self.screen.size_y:
            return

        if len(color) != 3 or color[0] > 255 or color[0] < 0 or color[1] > 255 or color[1] < 0 or color[2] > 255 or color[2] < 0:
            print("INVALID COLOR: ",color)

        # Sets the given pixel
        self.__pixels[self.__get_pixel_id_old(x, y) if Cfg.USE_OLD_WS2812B_CONNECTION_TYPE else self.__get_pixel_id(x, y)] = color

    def push_leds(self):
        self.__pixels.show()

    '''
    Method that takes in an x and y coordinate, calculates the exact pixel-id on the strip and returns it
    '''
    def __get_pixel_id_old(self, x: int, y: int):
        # Which box position on the wall this pixel belongs to
        # Pixel x = 7 would mean the 3rd box on the wall
        box_x = x // 3
        box_y = y // 4

        # Offset of the pixel from it's base box
        # x = 7 would mean an offset of 1
        offset_from_box_x = x - box_x * 3
        offset_from_box_y = y - box_y * 4

        # Calculates the amount of leds that got skipped by all boxes that came before the current one
        skipped_led_boxes = (box_x * Cfg.WALL_SIZE_Y + (
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
        )) * 3 * 4

        if offset_from_box_x == 2:
            return skipped_led_boxes + offset_from_box_y + 4

        factor = - offset_from_box_y * (1 if offset_from_box_x == 0 else 3)

        base = - int(offset_from_box_y < 2) * (10 if offset_from_box_x == 0 else 14)

        offset_range = 12 if offset_from_box_x == 0 else 17

        return skipped_led_boxes + factor + offset_range + base

    def __get_pixel_id(self, x: int, y: int):
        """
        Takes x and y Coordinates to find the corresponding LED on the Poxelbox arrangement.\n
        This approach first finds the corresponding Box by floor division and based on that the ID of the
        corresponding Box. The offset of the pixel then just misses the relative ID to that box, which is looked up
        based on the coordinates relative to its box.

        :param x: X-Coordinate of a pixel
        :param y: Y-Coordinate of a pixel
        :return: ID of the corresponding LED
        """

        # XY-Coordinates of the Box
        if Cfg.BOX_HORIZONTAL:
            box_x = x // Cfg.BOX_SIZE_Y
            box_y = y // Cfg.BOX_SIZE_X
        else:
            box_x = x // Cfg.BOX_SIZE_X
            box_y = y // Cfg.BOX_SIZE_Y

        # Number of Pixel that came before the box the pixel (x, y) ist located in
        # Columns that must have been skipped based on the X-coordinate
        box_px_offset = box_x * (Cfg.WALL_SIZE_Y * Cfg.PX_PER_BOX)

        # Handles the alternating direction of the XLR-cables
        if box_x % 2 == 0:
            # for even amounts of columns
            # box_px_offset directly corresponds to the Y-coordinate
            box_px_offset += box_y * Cfg.PX_PER_BOX

        else:
            # for odd amounts of columns
            # box_px_offset directly corresponds to the wall height minus Y-coordinate
            box_px_offset += (Cfg.WALL_SIZE_Y - 1 - box_y) * Cfg.PX_PER_BOX

        # The final ID is the offset of the Box plus the offset in the box itself
        if Cfg.BOX_HORIZONTAL:
            return box_px_offset + self.__rel_idx__(y % Cfg.BOX_SIZE_X, x % Cfg.BOX_SIZE_Y)
        return box_px_offset + self.__rel_idx__(x % Cfg.BOX_SIZE_X, y % Cfg.BOX_SIZE_Y)

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
            print("INVALID COLOR: ", color)
            return

        # Sets the given pixel
        self.__pixels[self.__get_pixel_id(x, y)] = color

    def push_leds(self):
        self.__pixels.show()

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
        box_offset = box_x * Cfg.WALL_SIZE_Y

        # Handles the alternating direction of the XLR-cables
        if box_x % 2 == 0:
            # for even amounts of columns
            # box_offset directly corresponds to the Y-coordinate
            box_offset += box_y

        else:
            # for odd amounts of columns
            # box_offset directly corresponds to the wall height minus Y-coordinate
            box_offset += Cfg.WALL_SIZE_Y - 1 - box_y

        # The final ID is the offset of the Box plus the offset in the box itself
        if Cfg.BOX_HORIZONTAL:
            return box_offset * Cfg.PX_PER_BOX + self.__rel_idx__(y % Cfg.BOX_SIZE_X, x % Cfg.BOX_SIZE_Y)
        return box_offset * Cfg.PX_PER_BOX + self.__rel_idx__(x % Cfg.BOX_SIZE_X, y % Cfg.BOX_SIZE_Y)

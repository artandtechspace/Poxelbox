from core.rendering.renderer.RendererBase import RendererBase
import board
import neopixel
import config.Config as Cfg


class WS2812BRenderer(RendererBase):
    # WS2812B-Access class
    __pixels: neopixel.NeoPixel

    def setup(self):
        super().setup()
        self.__pixels = neopixel.NeoPixel(board.D12, self.screen.size_x * self.screen.size_y, auto_write=False, pixel_order=neopixel.RGB)

    def set_led(self, x: int, y: int, color: (int, int, int)):
        # Ensures the position is on screen
        if x >= self.screen.size_x or y >= self.screen.size_y:
            return

        # Sets the given pixel
        self.__pixels[self.__get_pixel_id_old(x, y) if Cfg.USE_OLD_WS2812B_CONNECTION_TYPE else self.__get_pixel_id(x, y)] = color

    def push_leds(self):
        self.__pixels.show()

    '''
    (Old/Deprecated) Method that takes in an x and y coordinate, calculates the exact pixel-id on the strip and returns it
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

        is_origin_at_bottom = box_x % 2 == 0

        mapped_x_offset = offset_from_box_x if is_origin_at_bottom else (2 - offset_from_box_x)

        origin_direction = -1 if is_origin_at_bottom else 1

        if mapped_x_offset == 2:
            return skipped_led_boxes + offset_from_box_y * -origin_direction + (4 if is_origin_at_bottom else 7)

        is_upper_layer = offset_from_box_y >= 2
        upper_layer_disabler = 0 if is_upper_layer else 1

        is_x_offset_0 = mapped_x_offset == 0

        factor = 1 if is_x_offset_0 else 3

        base = 10 if is_x_offset_0 else 14

        offset_range = (
            (12 if is_origin_at_bottom else -1)
            if is_x_offset_0 else
            (17 if is_origin_at_bottom else -6)
        )

        return skipped_led_boxes + factor * origin_direction * offset_from_box_y + offset_range + base * origin_direction * upper_layer_disabler

    '''
    Method that takes in an x and y coordinate, calculates the exact pixel-id on the strip and returns it
    '''
    def __get_pixel_id(self, x: int, y: int):
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

        mapped_x_offset = offset_from_box_x

        if mapped_x_offset == 2:
            return skipped_led_boxes + offset_from_box_y + 4

        is_upper_layer = offset_from_box_y >= 2
        upper_layer_disabler = 0 if is_upper_layer else 1

        is_x_offset_0 = mapped_x_offset == 0

        factor = 1 if is_x_offset_0 else 3

        base = 10 if is_x_offset_0 else 14

        offset_range = 12 if is_x_offset_0 else 17

        return skipped_led_boxes + -factor * offset_from_box_y + offset_range + -base * upper_layer_disabler

    def __new_get_pixel_id(self, x: int, y: int):
        """
        Takes x and y Coordinates to find the corresponding LED on the Poxelbox arrangement.\n
        This approach first finds the corresponding Box by floor division and based on that the ID of the
        corresponding Box. The offset of the pixel then just misses the relative ID to that box, which is looked up
        based on the coordinates relative to its box.

        :param x: X-Coordinate of a pixel
        :param y: Y-Coordinate of a pixel
        :return: ID of the corresponding LED
        """
        # TODO: allow multiple orientations
        LED_IDX = [[8, 9, 10],
                   [7, 12, 11],
                   [6, 1, 2],
                   [5, 4, 3]]

        # XY-Coordinates of the Box
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
            box_px_offset += Cfg.WALL_SIZE_Y * Cfg.PX_PER_BOX - box_y * Cfg.PX_PER_BOX

        # The final ID is the offset of the Box plus the offset in the box itself
        no_px = box_px_offset + LED_IDX[x % Cfg.BOX_SIZE_X][y % Cfg.BOX_SIZE_Y]
        return no_px

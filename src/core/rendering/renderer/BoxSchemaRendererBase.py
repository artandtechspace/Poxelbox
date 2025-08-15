from core.rendering.renderer.RendererBase import RendererBase
import config.Config as Cfg

rel_idx = lambda rel_x, rel_y: (rel_y + 4) if rel_x == 2 else \
    12 - rel_y + rel_x * (5 - 2 * rel_y) + int(rel_y < 2) * (-10 - 4 * rel_x)


class BoxSchemaRendererBase(RendererBase):

    def __init__(self):
        super().__init__()
        self.__rel_idx__: callable = None

    def setup(self):
        super().setup()

        global rel_idx

        # TOD0: Allow different orientations for each box

        if Cfg.BOX_HORIZONTAL:
            Cfg.BOX_FLIPPED_H = not Cfg.BOX_FLIPPED_H

        if Cfg.BOX_FLIPPED_H:  # (X | Y)
            if Cfg.BOX_FLIPPED_V:
                self.__rel_idx__ = rel_idx
            else:
                self.__rel_idx__ = lambda rel_x, rel_y: rel_idx(rel_x, Cfg.BOX_SIZE_Y - 1 - rel_y)
        else:  # (-X | Y)
            if Cfg.BOX_FLIPPED_V:
                self.__rel_idx__ = lambda rel_x, rel_y: rel_idx(Cfg.BOX_SIZE_X - 1 - rel_x, rel_y)
            else:
                self.__rel_idx__ = lambda rel_x, rel_y: rel_idx(Cfg.BOX_SIZE_X - 1 - rel_x, Cfg.BOX_SIZE_Y - 1 - rel_y)

    def set_box_schema_led(self, idx: int, color: (int, int, int)):
        """
        Takes in the box-schema index and the color to set that pixel to.
        This method should be overwritten by the subclasses
        """
        pass

    def set_led(self, x: int, y: int, color: (int, int, int)):
        color = super(x, y, color) # brightess adjusted color
        if not color: # fade in abort
            return
        # TODO: Implement better logging here

        # Ensures the position is on screen
        if x >= self.screen.size_x or y >= self.screen.size_y or x < 0 or y < 0:
            print("Out of range!!! x:", x, " y:", y)
            return

        # Ensures that the color is valid
        if len(color) != 3 or color[0] > 255 or color[0] < 0 or color[1] > 255 or color[1] < 0 or color[2] > 255 or \
                color[2] < 0:
            print("INVALID COLOR: ", color)
            return

        # Sets the given pixel
        self.set_box_schema_led(self.__get_pixel_id(x, y), color)

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

    def push_leds():
        super()

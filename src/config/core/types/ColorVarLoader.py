from config.core.types.BaseVarLoader import BaseVarLoader


def color_to_hex(color):
    return color[0] << 16 | color[1] << 8 | color[2]


def hex_to_color(raw_number):
    r = raw_number >> 16
    g = raw_number >> 8 & 0xff
    b = raw_number & 0xff

    return r, g, b


class ColorVarLoader(BaseVarLoader):

    def __init__(self, var_name: str, presets: [int] = None):
        super().__init__(var_name)

        self.presets = presets

    def to_json(self):
        # Converts from hex-color to tuple
        return color_to_hex(super().to_json())

    def from_json(self, new_value):
        # Checks type
        if not isinstance(new_value, int):
            return

        # Ensures that the element is valid (Contained inside the list)
        if new_value not in self.presets:
            return

        # Converts from tuple to a hex-color
        super().from_json(hex_to_color(new_value))

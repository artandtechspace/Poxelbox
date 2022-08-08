import config.core.types.BaseVarLoader as BaseVL
import config.core.ConfigLoader as CfgLdr

def _color_to_hex(color):
    return color[0] << 16 | color[1] << 8 | color[2]


def _hex_to_color(raw_number):
    r = raw_number >> 16
    g = raw_number >> 8 & 0xff
    b = raw_number & 0xff

    return r, g, b


class ColorVLBuilder(BaseVL.BaseVLBuilder):

    def __init__(self, back_ref: CfgLdr.CategoryBuilder, var_name: str):
        super().__init__(back_ref, var_name)

    def export_end(self):
        return ColorVarLoader(self._var_name, self._title, self._description)


class ColorVarLoader(BaseVL.BaseVarLoader):

    def __init__(self, var_name: str, title: str = None, description: str = None):
        super().__init__(var_name, title, description)

    def get_type(self):
        return "color"

    def to_json(self):
        # Converts from hex-color to tuple
        return _color_to_hex(super().to_json())

    def from_json(self, new_value):
        # Checks type
        if not isinstance(new_value, int):
            return False

        # Converts from tuple to a hex-color
        return super().from_json(_hex_to_color(new_value))

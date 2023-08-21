import config.core.types.BaseVarLoader as BaseVL
import config.core.ConfigLoader as CfgLdr

class IntPresetVLBuilder(BaseVL.BaseVLBuilder):

    __presets: [int]

    def __init__(self, back_ref: CfgLdr.CategoryBuilder, var_name: str, presets: [int]):
        super().__init__(back_ref, var_name)

        self.__presets = presets

    def export_end(self):
        return IntPresetVarLoader(self._var_name, self._title, self._description, self._link, self.__presets)

class IntPresetVarLoader(BaseVL.BaseVarLoader):

    presets: [int]

    def __init__(self, var_name: str, title: str = None, description: str = None, link: str = None, presets: [int] = None):
        super().__init__(var_name, title, description, link)

        self.presets = presets

    def get_type(self):
        return "int_preset"

    def export_full(self):
        return super().export_full() | {
            "presets": self.presets
        }

    def validate_value(self, new_value):
        # Checks type
        if not isinstance(new_value, int):
            return False

        # Ensures that the element is valid (Contained inside the list)
        if new_value not in self.presets:
            return False

        return super().validate_value(new_value)

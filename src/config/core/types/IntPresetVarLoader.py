from config.core.types.BaseVarLoader import BaseVarLoader


class IntPresetVarLoader(BaseVarLoader):

    presets: [int]

    def __init__(self, var_name: str, presets: [int] = None):
        super().__init__(var_name)

        self.presets = presets

    def from_json(self, new_value):
        # Checks type
        if not isinstance(new_value, int):
            return

        # Ensures that the element is valid (Contained inside the list)
        if new_value not in self.presets:
            return

        super().from_json(new_value)

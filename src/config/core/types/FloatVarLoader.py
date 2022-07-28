from config.core.types.BaseVarLoader import BaseVarLoader


class FloatVarLoader(BaseVarLoader):

    min: int
    max: int

    def __init__(self, var_name: str, min: int=None, max: int=None):
        super().__init__(var_name)

        self.min = min
        self.max = max

    def from_json(self, new_value):
        # Checks type
        if not isinstance(new_value, float):
            return

        # Checks min
        if self.min is not None and new_value < self.min:
            new_value = self.min

        # Checks max
        if self.max is not None and new_value > self.max:
            new_value = self.max

        super().from_json(new_value)

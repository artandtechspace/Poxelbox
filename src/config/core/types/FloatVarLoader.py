import config.core.types.BaseVarLoader as BaseVL
import config.core.ConfigLoader as CfgLdr


class FloatVLBuilder(BaseVL.BaseVLBuilder):
    __min: float
    __max: float

    def __init__(self, back_ref: CfgLdr.CategoryBuilder, var_name: str):
        super().__init__(back_ref, var_name)

    def has_min(self, min: float):
        self.__min = min
        return self

    def has_max(self, max: float):
        self.__max = max
        return self

    def export_end(self):
        return FloatVarLoader(self._var_name, self._title, self._description, self._link, self.__min, self.__max)


class FloatVarLoader(BaseVL.BaseVarLoader):
    min: float
    max: float

    def __init__(self, var_name: str, title: str = None, description: str = None, link: str = None, min: float = None, max: float = None):
        super().__init__(var_name, title, description, link)

        self.min = min
        self.max = max

    def get_type(self):
        return "float"

    def export_full(self):
        return super().export_full() | {
            "min": self.min,
            "max": self.max
        }

    def validate_value(self, new_value):
        if isinstance(new_value, int):
            new_value = float(new_value)

        # Checks type
        if not isinstance(new_value, float):
            return False

        # Checks min
        if self.min is not None and new_value < self.min:
            new_value = self.min

        # Checks max
        if self.max is not None and new_value > self.max:
            new_value = self.max

        return super().validate_value(new_value)

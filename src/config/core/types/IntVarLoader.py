import config.core.types.BaseVarLoader as BaseVL
import config.core.ConfigLoader as CfgLdr

class IntVLBuilder(BaseVL.BaseVLBuilder):

    __min: int
    __max: int

    def __init__(self, back_ref: CfgLdr.CategoryBuilder, var_name: str):
        super().__init__(back_ref, var_name)

    def has_min(self, min: int):
        self.__min = min
        return self

    def has_max(self, max: int):
        self.__max = max
        return self

    def export_end(self):
        return IntVarLoader(self._var_name, self._title, self._description, self._link, self.__min, self.__max)

class IntVarLoader(BaseVL.BaseVarLoader):
    min: int
    max: int

    def __init__(self, var_name: str, title: str = None, description: str = None, link: str = None, min: int = None, max: int = None):
        super().__init__(var_name, title, description, link)

        self.min = min
        self.max = max

    def get_type(self):
        return "int"

    def export_full(self):
        return super().export_full() | {
            "min": self.min,
            "max": self.max
        }

    def validate_value(self, new_value):
        # Checks type
        if not isinstance(new_value, int):
            return False

        # Checks min
        if self.min is not None and new_value < self.min:
            new_value = self.min

        # Checks max
        if self.max is not None and new_value > self.max:
            new_value = self.max

        return super().validate_value(new_value)

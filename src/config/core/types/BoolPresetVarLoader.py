import config.core.types.BaseVarLoader as BaseVL
import config.core.ConfigLoader as CfgLdr

class BoolVLBuilder(BaseVL.BaseVLBuilder):

    def __init__(self, back_ref: CfgLdr.CategoryBuilder, var_name: str):
        super().__init__(back_ref, var_name)

    def export_end(self):
        return BoolVarLoader(self._var_name, self._title, self._description)

class BoolVarLoader(BaseVL.BaseVarLoader):

    def __init__(self, var_name: str, title: str = None, description: str = None):
        super().__init__(var_name, title, description)

    def get_type(self):
        return "bool"

    def from_json(self, new_value):
        # Checks type
        if not isinstance(new_value, bool):
            return False

        return super().from_json(new_value)

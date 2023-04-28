import config.Config as Cfg
import config.core.ConfigLoader as CfgLdr

class BaseVLBuilder:
    # Basic stats of the var-loader
    _var_name: str
    _title: str
    _description: str

    # Reference back to the config-loader-builder
    __back_ref: CfgLdr.CategoryBuilder

    def __init__(self, back_ref: CfgLdr.CategoryBuilder, var_name: str):
        self._var_name = var_name
        self.__back_ref = back_ref
        self._title = None

    # Uses to set a title to the config-value
    def has_title(self, title: str):
        self._title = title
        return self

    # Uses to set a description to the config-value
    def has_description(self, desc: str):
        self._description = desc
        return self

    # Continues to add more values
    def and_then(self):
        return self.__back_ref

    # Used to finally convert into an actual var-loader
    # This must be implemented inside a subclass
    def export_end(self):
        raise NotImplementedError()


class BaseVarLoader:
    # Name of the variable on the config-file
    __var_name: str
    __title: str
    __description: str
    __type: str

    def __init__(self, var_name: str, title: str = None, description: str = None):
        self.__var_name = var_name
        self.__title = title
        self.__description = description

    def get_type(self):
        raise NotImplementedError()

    # Return the current value from the config as json-exportable
    def to_json(self):
        return getattr(Cfg, self.__var_name)

    # Convert a json-read-value to the actual config value and sets it
    def from_json(self, new_value) -> bool:
        setattr(Cfg, self.__var_name, new_value)
        return True

    # Used to export all settings that are required on the frontend for setup
    def export_full(self):
        return {
            "value": self.to_json(),
            "title": self.__title,
            "desc": self.__description,
            "type": self.get_type()
        }

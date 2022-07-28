import config.Config as Cfg


class BaseVarLoader:
    # Name of the variable on the config-file
    __var_name: str

    def __init__(self, var_name: str):
        self.__var_name = var_name

    # Return the current value from the config as json-exportable
    def to_json(self):
        return getattr(Cfg, self.__var_name)

    # Convert a json-read-value to the actual config value and sets it
    def from_json(self, new_value):
        setattr(Cfg, self.__var_name, new_value)
        pass

    # Used to export all settings that are required on the frontend for setup
    def export_full(self):
        return {
            "value": self.to_json()
        }

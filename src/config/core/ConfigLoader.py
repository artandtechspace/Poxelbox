import json
from config.core.types.BaseVarLoader import BaseVarLoader
from config.core.types.IntPresetVarLoader import IntPresetVarLoader
from config.core.types.ColorVarLoader import ColorVarLoader
from config.core.types.FloatVarLoader import FloatVarLoader
from config.core.types.IntVarLoader import IntVarLoader


class ConfigLoader:
    # Holds all registered config-loaders
    __values: {BaseVarLoader} = {}

    # Takes in a raw json-string and tries to load the config-values based on that
    # Returns false if the json-string is invalid
    def try_load_from_json(self, raw_json: str):
        try:
            # Tries to load the json
            loaded = json.loads(raw_json)

            # Iterates over all loaded  values
            for key in loaded:
                # Ensures the settings exists
                if key in self.__values:
                    # Tries to update the value
                    self.__values[key].from_json(loaded[key])
            return True

        except:
            return False

    # Used to convert all current settings to a json-string
    def export_to_json(self):
        exp = {}

        for key in self.__values:
            exp[key] = self.__values[key].to_json()

        return json.dumps(exp)

    def register_int(self, var_name: str, min: int = None, max: int = None):
        self.__values[var_name] = IntVarLoader(var_name, min, max)
        return self

    def register_float(self, var_name: str, min: float = None, max: float = None):
        self.__values[var_name] = FloatVarLoader(var_name, min, max)
        return self

    def register_color(self, var_name: str):
        self.__values[var_name] = ColorVarLoader(var_name)
        return self

    def register_int_preset(self, var_name: str, allowed: [int]):
        self.__values[var_name] = IntPresetVarLoader(var_name, allowed)
        return self

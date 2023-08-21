from __future__ import annotations
from typing import TYPE_CHECKING
import json
from core.util.DictUtil import delete_none

if TYPE_CHECKING:
    import config.core.types.IntVarLoader as IntVL
    import config.core.types.FloatVarLoader as FloatVL
    import config.core.types.ColorVarLoader as ColorVL
    import config.core.types.IntPresetVarLoader as IntPresetVL
    import config.core.types.StringPresetVarLoader as StringPresetVL
    import config.core.types.BoolVarLoader as BoolVL
    import config.core.types.BaseVarLoader as BaseVL


class CategoryBuilder:
    __builders: {BaseVL.BaseVLBuilder} = {}
    __base: ConfigLoaderBuilder

    def __init__(self, base: ConfigLoaderBuilder):
        self.__base = base
        self.__builders = {}

    def with_bool(self, var_name: str):
        import config.core.types.BoolVarLoader as BoolVL
        bdr = BoolVL.BoolVLBuilder(self, var_name)
        self.__builders[var_name] = bdr
        return bdr

    def with_int(self, var_name: str):
        import config.core.types.IntVarLoader as IntVL
        bdr = IntVL.IntVLBuilder(self, var_name)
        self.__builders[var_name] = bdr
        return bdr

    def with_float(self, var_name: str):
        import config.core.types.FloatVarLoader as FloatVL
        bdr = FloatVL.FloatVLBuilder(self, var_name)
        self.__builders[var_name] = bdr
        return bdr

    def with_string_preset(self, var_name: str, presets: [str]):
        import config.core.types.StringPresetVarLoader as StringPresetVL
        bdr = StringPresetVL.StringPresetVLBuilder(self, var_name, presets)
        self.__builders[var_name] = bdr
        return bdr

    def with_int_preset(self, var_name: str, presets: [int]):
        import config.core.types.IntPresetVarLoader as IntPresetVL
        bdr = IntPresetVL.IntPresetVLBuilder(self, var_name, presets)
        self.__builders[var_name] = bdr
        return bdr

    def with_color(self, var_name: str):
        import config.core.types.ColorVarLoader as ColorVL
        bdr = ColorVL.ColorVLBuilder(self, var_name)
        self.__builders[var_name] = bdr
        return bdr

    def end_category(self):
        return self.__base

    def export_end(self):
        values = {}

        for name in self.__builders:
            values[name] = self.__builders[name].export_end()

        return Category(values)


class ConfigLoaderBuilder:
    __categorys: {CategoryBuilder} = {}

    def __init__(self):
        self.__categorys = {}

    def in_category(self, name: str):
        bdr = CategoryBuilder(self)

        self.__categorys[name] = bdr

        return bdr

    def build(self):
        values = {}

        for name in self.__categorys:
            values[name] = self.__categorys[name].export_end()

        return ConfigLoader(values)


class Category:
    # Holds all registered variable-loaders
    __values: {BaseVL.BaseVarLoader} = {}

    def __init__(self, values: {BaseVL.BaseVarLoader}):
        self.__values = values

    # Exports all values so that they can be serialized as json
    # Returns python objects, not json objects
    def to_json(self):
        exp = {}

        for key in self.__values:
            exp[key] = self.__values[key].to_json()

        return exp

    # Exports all full values (Settings like min, max etc.) so that they can be serialized as json
    # Returns python objects, not json objects
    def to_json_full(self):
        exp = {}

        for key in self.__values:
            exp[key] = delete_none(self.__values[key].export_full())

        return exp

    def try_load_from_json(self, category_obj):
        if not isinstance(category_obj, dict):
            return False

        # Iterates over all given values
        for key in category_obj:
            # Ensures that the category exists and otherwise ignores it
            if key not in self.__values:
                continue

            # Tries to load
            # TODO: Stop ignoring errors
            success = self.__values[key].set_value(category_obj[key])

    # Takes in a raw category-object and validates it's values
    # Further the values that are missing are extended
    # If any of the given values is invalid, false is returned and if everything worked, true
    def validate_and_extend_json_config(self, category_obj) -> True or False:
        if not isinstance(category_obj, dict):
            return False

        # Iterates over all values
        for key in self.__values:
            # Ensures that the category exists and otherwise creates it
            if key not in category_obj:
                category_obj[key] = self.__values[key].get_value()

            # Validates the value
            if not self.__values[key].validate_value(category_obj[key]):
                return False

        return True


class ConfigLoader:
    # Holds all categories
    __categories: {Category} = {}

    def __init__(self, values: {Category}):
        self.__categories = values

    # Takes in a raw config object and validates it's values
    # Further the values that are missing are extended
    # If any of the given values is invalid, false is returned and if everything worked, true
    def validate_and_extend_json_config(self, raw_json: any or dict) -> True or False:
        if not isinstance(raw_json, dict):
            return False

            # Iterates over all given categories
        for cat_name in self.__categories:
            # Ensures that the category exists and otherwise creates it
            if cat_name not in raw_json:
                raw_json[cat_name] = {}

            # Tries to load and extends that category values. If false as in "invalid config given" is returned,
            # it is lead further up
            if not self.__categories[cat_name].validate_and_extend_json_config(raw_json[cat_name]):
                return False

        return True

    # Takes in a dict or invalid tuple (Parsed from json) and tries to load all config-values from it.
    # If the given json is not a dict, this just returns false
    def try_load_from_json(self, raw_json: dict | any):

        if not isinstance(raw_json, dict):
            return False

        # Iterates over all given categories
        for cat_name in raw_json:
            # Ensures that the category exists and otherwise ignores it
            if cat_name not in self.__categories:
                continue

            self.__categories[cat_name].try_load_from_json(raw_json[cat_name])

    # Used to generate a full export of all settings and their options (eg. min, max) as a json-string
    def export_full_to_json(self):
        exp = {}

        for cat_name in self.__categories:
            exp[cat_name] = self.__categories[cat_name].to_json_full()

        return json.dumps(exp)

    # Used to convert all current settings to a json-string
    def export_to_json(self):
        exp = {}

        for cat_name in self.__categories:
            exp[cat_name] = self.__categories[cat_name].to_json()

        return json.dumps(exp)

import config.Config as Cfg
import config.core.ConfigLoader as CfgLdr


class BaseVLBuilder:
    def __init__(self, back_ref: CfgLdr.CategoryBuilder, var_name: str):
        # Reference back to the config-loader-builder
        self.__back_ref = back_ref

        # Basic stats of the var-loader
        self._var_name = var_name
        self._title = None
        self._link = None
        self._description = None

    # Used to set a title to the config-value
    def has_title(self, title: str):
        self._title = title
        return self

    # Used to set a description to the config-value
    def has_description(self, desc: str):
        self._description = desc
        return self

    # Used to add an optional link that has an explanation for this property
    def has_link(self, link: str):
        self._link = link
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
    __link: str

    def __init__(self, var_name: str, title: str = None, description: str = None, link: str = None):
        self.__var_name = var_name
        self.__title = title
        self.__description = description
        self.__link = link

    def get_type(self):
        raise NotImplementedError()

    # Return the current value from the config as json-exportable
    def to_json(self):
        return getattr(Cfg, self.__var_name)

    # Takes in a value and returns if that value is valid
    def validate_value(self, new_value) -> bool:
        return True

    # Takes in a value, validates it and then sets it to the config
    # Also returns if that worked (The value was valid)
    def set_value(self, new_value) -> bool:
        if self.validate_value(new_value):
            setattr(Cfg, self.__var_name, new_value)
            return True
        return False

    # Returns the current value of the config-value
    def get_value(self):
        return getattr(Cfg, self.__var_name)

    # Used to export all settings that are required on the frontend for setup
    def export_full(self):
        return {
            "value": self.to_json(),
            "title": self.__title,
            "desc": self.__description,
            "type": self.get_type(),
            "link": self.__link if self.__link is not None else None
        }

import config.Config as Cfg
from config.core.ConfigLoader import ConfigLoader
from varname import nameof


# Event: When the config-loaders are registered
def register_on_loader():
    return ConfigLoader() \
        .register_int(nameof(Cfg.APP_SPEED), min=1, max=10) \
        .register_int(nameof(Cfg.LED_PIXEL_SCALE), min=5)\
        .register_int_preset(nameof(Cfg.ESP_BAUD), [115200, 9600])

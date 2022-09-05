import config.Config as Cfg
import config.core.ConfigLoader as CfgLdr
from varname import nameof


# Event: When the config-loaders are registered
def register_on_loader():
    return CfgLdr.ConfigLoaderBuilder()\
        \
        .in_category("Settings")\
        \
        .with_int(nameof(Cfg.APP_SPEED))\
        .has_min(1).has_max(10)\
        .has_title("Game-Speed")\
        .has_description("How fast the game is running")\
        .and_then()\
        \
        .with_int(nameof(Cfg.LED_PIXEL_SCALE))\
        .has_min(5)\
        .has_max(100)\
        .has_title("PyGame-Pixel-Scale")\
        .has_description("How many Screen-Pixel one Game-Pixel uses")\
        .and_then()\
        \
        .with_int_preset(nameof(Cfg.ESP_BAUD), [115200, 9600])\
        .has_title("Esp-Baud")\
        .has_description("Baud-rate that is used to communicate with the Esp32")\
        .and_then()\
        \
        .with_int(nameof(Cfg.WALL_SIZE_X))\
        .has_min(1)\
        .has_max(10)\
        .has_title("Wall-Size (X)")\
        .has_description("Of how many cubes (on the x axis) does the wall consist?")\
        .and_then()\
        \
        .with_int(nameof(Cfg.WALL_SIZE_Y))\
        .has_min(1)\
        .has_max(10)\
        .has_title("Wall-Size (Y)")\
        .has_description("Of how many cubes (on the y axis) does the wall consist?")\
        .and_then()\
        \
        .end_category()\
        .build()

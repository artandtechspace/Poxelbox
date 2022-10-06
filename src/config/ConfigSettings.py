import config.Config as Cfg
import config.core.ConfigLoader as CfgLdr
from varname import nameof


# Event: When the config-loaders are registered
def register_on_loader():
    return CfgLdr.ConfigLoaderBuilder()\
        \
        .in_category("Settings")\
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
        .with_bool(nameof(Cfg.IS_DEVELOPMENT_ENVIRONMENT))\
        .has_title("Is Dev-Environment?")\
        .has_description("Is the software running in development (True) or production (False) mode?")\
        .and_then()\
        \
        .with_bool(nameof(Cfg.USE_TEST_SCENE))\
        .has_title("Use test scene?")\
        .has_description("Shall the test-screen-scene be loaded instead of the normal start scene?")\
        .and_then()\
        \
        .with_float(nameof(Cfg.TETRIS_SPEED))\
        .has_min(0)\
        .has_max(1)\
        .has_title("Speed (Tetris)")\
        .has_description("Delay in ms between frames in tetris.")\
        .and_then()\
        \
        .with_float(nameof(Cfg.SNAKE_SPEED))\
        .has_min(0)\
        .has_max(1)\
        .has_title("Speed (Snake)")\
        .has_description("Delay in ms between frames in snake.")\
        .and_then()\
        \
        .with_float(nameof(Cfg.PONG_SPEED))\
        .has_min(0)\
        .has_max(1)\
        .has_title("Speed (Pong)")\
        .has_description("Delay in ms between frames in pong.")\
        .and_then()\
        \
        .with_bool(nameof(Cfg.USE_OLD_WS2812B_CONNECTION_TYPE))\
        .has_description("If the old ws2812b connection schema or the new one should be used.")\
        .has_title("Use old WS2812B-Schema?")\
        .and_then()\
        \
        .end_category()\
        .build()

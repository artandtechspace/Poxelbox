import config.Config as Cfg
import config.core.ConfigLoader as CfgLdr
from varname import nameof


def register_snake_loader(loader: CfgLdr.ConfigLoaderBuilder):
    return loader.in_category("Game-Snake") \
        .with_bool(nameof(Cfg.SNAKE_ENABLED)) \
        .has_title("Snake enabled") \
        .has_description("If snake is selectable and playable.") \
        .and_then() \
        .with_float(nameof(Cfg.SNAKE_SPEED)) \
        .has_min(0) \
        .has_max(1) \
        .has_title("Speed") \
        .has_description("Delay in ms between frames in snake.") \
        .and_then() \
        .end_category()


def register_pong_loader(loader: CfgLdr.ConfigLoaderBuilder):
    return loader.in_category("Game-Pong") \
        .with_bool(nameof(Cfg.PONG_ENABLED)) \
        .has_title("Pong enabled") \
        .has_description("If pong is selectable and playable.") \
        .and_then() \
        .with_float(nameof(Cfg.PONG_SPEED)) \
        .has_min(0) \
        .has_max(1) \
        .has_title("Speed") \
        .has_description("Delay in ms between frames in pong.") \
        .and_then() \
        .end_category()


def register_tetris_loader(loader: CfgLdr.ConfigLoaderBuilder):
    return loader.in_category("Game-Tetris") \
        .with_bool(nameof(Cfg.TETRIS_ENABLED)) \
        .has_title("Tetris enabled") \
        .has_description("If tetris is selectable and playable.") \
        .and_then() \
 \
        .with_float(nameof(Cfg.TETRIS_SPEED)) \
        .has_min(0) \
        .has_max(1) \
        .has_title("Speed") \
        .has_description("Delay in ms between frames in tetris.") \
        .and_then() \
        .end_category()


def register_minesweeper_loader(loader: CfgLdr.ConfigLoaderBuilder):
    return loader.in_category("Game-Minesweeper") \
        .with_bool(nameof(Cfg.MINESWEEPER_ENABLED)) \
        .has_title("Minesweeper enabled") \
        .has_description("If minesweeper is selectable and playable.") \
        .and_then() \
        .end_category()


def register_draw_loader(loader: CfgLdr.ConfigLoaderBuilder):
    return loader.in_category("Animation-Draw") \
        .with_bool(nameof(Cfg.DRAW_ENABLED)) \
        .has_title("Draw enabled") \
        .has_description("If the draw-animation is enabled") \
        .and_then() \
        .end_category()


def register_rgb_spiral_loader(loader: CfgLdr.ConfigLoaderBuilder):
    return loader.in_category("Animation-RGB-Spiral") \
        .with_bool(nameof(Cfg.RGB_SPIRAL_ENABLED)) \
        .has_title("RGB-Spiral enabled") \
        .has_description("If the rgb-spiral-animation is enabled") \
        .and_then() \
        .end_category()


def register_box_layout(loader: CfgLdr.ConfigLoaderBuilder):
    return loader.in_category("Box-layout") \
        .with_int(nameof(Cfg.WALL_SIZE_X)) \
        .has_min(1) \
        .has_max(10) \
        .has_title("Wall-Size (X)") \
        .has_description("Of how many cubes (on the x axis) does the wall consist?") \
        .has_link("https://github.com/artandtechspace/Poxelbox-Dokumentation#wall-size-xy") \
        .and_then() \
 \
        .with_int(nameof(Cfg.WALL_SIZE_Y)) \
        .has_min(1) \
        .has_max(10) \
        .has_title("Wall-Size (Y)") \
        .has_description("Of how many cubes (on the y axis) does the wall consist?") \
        .has_link("https://github.com/artandtechspace/Poxelbox-Dokumentation#wall-size-xy") \
        .and_then() \
 \
        .with_bool(nameof(Cfg.BOX_FLIPPED_H)) \
        .has_description("Inverts the relative x-coordinates for each box") \
        .has_title("Flip each box over the y-axis") \
        .and_then() \
 \
        .with_bool(nameof(Cfg.BOX_FLIPPED_V)) \
        .has_description("Inverts the relative y-coordinates for each box") \
        .has_title("Flip each box over the x-axis") \
        .has_link("https://github.com/artandtechspace/Poxelbox-Dokumentation#flip-each-box-over-y-axis-or-x-axis") \
        .and_then() \
 \
        .with_bool(nameof(Cfg.BOX_HORIZONTAL)) \
        .has_description("Is the longer side of the boxes parallel to the ground?") \
        .has_title("Are boxes placed horizontal?") \
        .has_link("https://github.com/artandtechspace/Poxelbox-Dokumentation#flip-each-box-over-y-axis-or-x-axis") \
        .and_then() \
 \
        .end_category()


def register_settings_loader(loader: CfgLdr.ConfigLoaderBuilder):
    return loader.in_category("General-Settings") \
 \
        .with_int(nameof(Cfg.LED_PIXEL_SCALE)) \
        .has_min(5) \
        .has_max(100) \
        .has_title("PyGame-Pixel-Scale") \
        .has_description("How many Screen-Pixel one Game-Pixel uses") \
        .has_link("https://github.com/artandtechspace/Poxelbox-Dokumentation#pygame-pixel-scale") \
        .and_then() \
 \
        .with_int_preset(nameof(Cfg.ESP_BAUD), [115200, 9600]) \
        .has_title("Esp-Baud") \
        .has_description("Baud-rate that is used to communicate with the Esp32") \
        .has_link("https://github.com/artandtechspace/Poxelbox-Dokumentation#esp-baud") \
        .and_then() \
 \
        .with_bool(nameof(Cfg.IS_DEVELOPMENT_ENVIRONMENT)) \
        .has_title("Is Dev-Environment?") \
        .has_description("Is the software running in development (True) or production (False) mode?") \
        .has_link("https://github.com/artandtechspace/Poxelbox-Dokumentation#is-dev-environment") \
        .and_then() \
 \
        .with_bool(nameof(Cfg.USE_TEST_SCENE)) \
        .has_title("Use test scene?") \
        .has_description("Shall the test-screen-scene be loaded instead of the normal start scene?") \
        .has_link("https://github.com/artandtechspace/Poxelbox-Dokumentation#use-test-scene") \
        .and_then() \
 \
        .end_category()


# Event: When the config-loaders are registered
def register_on_loader():
    loader = CfgLdr.ConfigLoaderBuilder()

    loader = register_settings_loader(loader)
    loader = register_box_layout(loader)
    loader = register_snake_loader(loader)
    loader = register_pong_loader(loader)
    loader = register_tetris_loader(loader)
    loader = register_minesweeper_loader(loader)
    loader = register_rgb_spiral_loader(loader)
    loader = register_draw_loader(loader)

    return loader.build()

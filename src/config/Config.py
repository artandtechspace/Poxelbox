'''
!Important!
Always import the whole Config module using
import config.Config as Cfg
because otherwise overriding config-values wont take effect for your code
'''

'''
Snake settings
'''
SNAKE_ENABLED = True
SNAKE_SPEED = 0.15

SNAKE_WALL_DEAD = False

'''
Tetris settings
'''
TETRIS_ENABLED = True
TETRIS_SPEED = 0.2

'''
Minesweeper settings
'''
MINESWEEPER_ENABLED = True

'''
Draw settings
'''
DRAW_ENABLED = True

'''
RGB-Spiral settings
'''
RGB_SPIRAL_ENABLED = True

'''
Pong settings
'''
PONG_ENABLED = True
PONG_SPEED = 0.1

'''
Rendering settings
'''
RENDERER_FADE_IN_FRAMES: int = 30
RENDERER_FADE_IN_DURATION: float = 1 # in seconds
# Brightness:
# in range [0, 1] where 0 ~ black; 1 ~ unchanged color
RENDERER_BRIGHTNESS_SCALED_LIMIT: float = 0.5 # scales all colors
RENDERER_BRIGHTNESS_HARD_LIMIT: float = 1.0 # limits maximal brightness


# How many screen-pixels one poxel-pixel takes up on the pygame-renderer
LED_PIXEL_SCALE = 30

# Serial-Baud rate that the esp32 uses for the serial-userinput connection
ESP_BAUD = 9600

# Amount of cubes the wall consists of
WALL_SIZE_X = 6
WALL_SIZE_Y = 6

# Orientation and alignment of the boxes
BOX_HORIZONTAL = False
BOX_FLIPPED_H = False
BOX_FLIPPED_V = False

# Dimensions of one Box
BOX_SIZE_X = 3
BOX_SIZE_Y = 4
PX_PER_BOX = BOX_SIZE_X * BOX_SIZE_Y

# If on dev (True) or on pi (False)
IS_DEVELOPMENT_ENVIRONMENT = False

# If the test-scene scene shall be used when running the software
USE_TEST_SCENE = False

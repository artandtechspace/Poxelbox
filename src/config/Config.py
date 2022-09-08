'''
!Important!
Allways import the whole Config module using
import config.Config as Cfg
because otherwise overriding config-values wont take effect for your code
'''

# How many screen-pixels one poxel-pixel takes up on the pygame-renderer
LED_PIXEL_SCALE = 60

# Serial-Baud rate that the esp32 uses for the serial-userinput connection
ESP_BAUD = 9600

# General speed of all scenes. Default is normal 1
APP_SPEED = 1

# Amount of cubes the wall consists of
WALL_SIZE_X = 6
WALL_SIZE_Y = 6

# If on dev (True) or on pi (False)
IS_DEVELOPMENT_ENVIRONMENT = False

# If the test-scene scene shall be used when running the software
USE_TEST_SCENE = False

# Speed of the games
TETRIS_SPEED = 0.2
PONG_SPEED = 0.1
SNAKE_SPEED = 0.15

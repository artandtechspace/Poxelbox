import pygame
import config.ControllerKeys as Keys

# How many screen-pixel one poxel-pixel takes up on the pygame-renderer
PyGameRenderer_LED_PIXEL_SCALE = 60

# Serial-Baud rate that the esp32 uses for the serial-userinput connection
SerialEspUserInput_ESP_BAUD = 9600

# General speed of all scenes. Default is normal 1
Scene_SPEED = 1

# Key-mappings from pygame-keys to play-keys
# Mappings for player one
PyGameUserInput_KEY_MAPPINGS_P1 = {
    pygame.K_c: Keys.BTN_A,
    pygame.K_v: Keys.BTN_B,
    pygame.K_a: Keys.BTN_LEFT,
    pygame.K_w: Keys.BTN_UP,
    pygame.K_d: Keys.BTN_RIGHT,
    pygame.K_s: Keys.BTN_DOWN,
    pygame.K_t: Keys.BTN_SELECT,
    pygame.K_z: Keys.BTN_START
}

# Mappings for player two
PyGameUserInput_KEY_MAPPINGS_P2 = {
    pygame.K_k: Keys.BTN_A,
    pygame.K_l: Keys.BTN_B,
    pygame.K_LEFT: Keys.BTN_LEFT,
    pygame.K_UP: Keys.BTN_UP,
    pygame.K_RIGHT: Keys.BTN_RIGHT,
    pygame.K_DOWN: Keys.BTN_DOWN,
    pygame.K_o: Keys.BTN_SELECT,
    pygame.K_p: Keys.BTN_START
}
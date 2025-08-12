from core.rendering.renderer.RendererBase import RendererBase
import config.Config as Cfg
import time

class configuration:
    FADE_IN_FRAMES: int = 30
    FADE_IN_DURATION: float = 1 # in seconds
    pass

#region Helperfunctions

@staticmethod
def lerp( color_a: (int, int, int), color_b: (int, int, int), t: float ):
    return tuple( a * (1-t) + b * t for a, b in zip(color_a, color_b) )

@staticmethod
def set_color_brightness(color: (int, int, int), brightness: float):
    return lerp( (0, 0, 0), color, brightness )

#endregion

class BrightnessControlledAndOptionalFadeInRenderer(RendererBase):
    
    is_capturing_screen : bool = False
    caputured_set_led_calls: [int] = []

    def __init__(self):
        super().__init__()
    
    def setup(self):
        super().setup()

    def start_fade_in_until_nex_flush(self):
        self.caputured_set_led_calls = []
        self.is_capturing_screen = True

    def set_led(self, x: int, y: int, color: (int, int, int)):
        if self.is_capturing_screen:
            self.caputured_set_led_calls.append((x, y, color))
            return False
        return True

    def __set_brightness(self, brightness : float, color: (int, int, int)):
        # brightness = min(0, max(1, brightness))
        pass

    def push_leds(self):
        sleep_duration = configuration.FADE_IN_DURATION / configuration.FADE_IN_FRAMES
        for i in range(configuration.FADE_IN_FRAMES):
            for caputured_call in self.caputured_set_led_calls:
                self.set_led(
                        caputured_call[0],
                        caputured_call[1],
                        set_color_brightness(caputured_call[2], i/configuration.FADE_IN_FRAMES)
                )
            time.sleep(sleep_duration)
        self.caputured_set_led_calls = []
        self.is_capturing_screen = False

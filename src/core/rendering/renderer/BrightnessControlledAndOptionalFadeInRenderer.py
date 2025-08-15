from core.rendering.renderer.RendererBase import RendererBase
import config.Config as Cfg
import time

class configuration:
    RENDERER_FADE_IN_FRAMES: int = 30
    RENDERER_FADE_IN_DURATION: float = 1 # in seconds
    # in range [0, 1] where 0 ~ black; 1 ~ unchanged color
    RENDERER_BRIGHTNESS_MAXVALUE: float = 1.0

#region Helperfunctions

@staticmethod
def lerp( color_a: (int, int, int), color_b: (int, int, int), t: float ):
    return tuple( int(a * (1-t) + b * t) for a, b in zip(color_a, color_b) )

@staticmethod
def set_color_brightness(color: (int, int, int), brightness: float):
    # conceptually the same as: 
    # return lerp( (0, 0, 0), color, brightness )
    return tuple( int(b * t) for b in color )

@staticmethod
def clamp(lower_bound, upper_bound, value):
    return min( lower_bound, max(upper_bound, value))

#endregion

class BrightnessControlledAndOptionalFadeInRenderer(RendererBase):
    
    is_capturing_screen : bool = False
    caputured_set_led_calls: [int] = []

    def __init__(self):
        super().__init__()
    
    def setup(self):
        super().setup()

    def start_capture_for_fade_in(self):
        self.caputured_set_led_calls = []
        self.is_capturing_screen = True

    def set_led(self, x: int, y: int, color: (int, int, int)):
        """
        in child overrides:
        color = super(x, y, color) # brightess adjusted color
        if not color: # fade in abort
            return
        """
        if self.is_capturing_screen:
            # NOTE does override old capture when set_led is called on the same coordinate
            self.caputured_set_led_calls.append((x, y, color))
            return False
        return set_color_brightness(color=color, brightness=configuration.RENDERER_BRIGHTNESS_MAXVALUE)

    def push_leds(self):
        pass
    
    def play_fade_in(self):
        if not (self.is_capturing_screen and self.caputured_set_led_calls):
            return
        self.is_capturing_screen = False
        sleep_duration = configuration.RENDERER_FADE_IN_DURATION / configuration.RENDERER_FADE_IN_FRAMES
        for i in range(configuration.RENDERER_FADE_IN_FRAMES):
            for caputured_call in self.caputured_set_led_calls:
                self.set_led(
                        caputured_call[0],
                        caputured_call[1],
                        set_color_brightness(caputured_call[2], i/configuration.RENDERER_FADE_IN_FRAMES)
                )
            self.push_leds()
            time.sleep(sleep_duration)
        self.caputured_set_led_calls = []

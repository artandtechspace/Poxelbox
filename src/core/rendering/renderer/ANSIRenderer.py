from core.rendering.renderer.RendererBase import RendererBase
import sys


class ANSIRenderer(RendererBase):

    def setup(self):
        super().setup()
        # Clears the screen and disables the cursor
        sys.stdout.write("\x1b[2J\x1b[?25l")

    def set_led(self, x: int, y: int, color: (int, int, int)):
        color = super().set_led(x, y, color) # brightess adjusted color
        if not color: # fade in abort
            return
        # Moves to the position and write the color
        sys.stdout.write(
            "\x1b[" + str(y) + ";" + str(x) + "H\x1b[48;2;" + str(color[0]) + ";" + str(color[1]) + ";" + str(
                color[2]) + "m ")
        pass

    def push_leds(self):
        sys.stdout.flush()
        pass

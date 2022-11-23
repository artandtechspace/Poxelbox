from core.rendering.animations.AnimationBase import AnimationBase
from core.util.Vector2D import Vector2D
from core.rendering.renderer.RendererBase import RendererBase
import time


class AnimatedPixel(AnimationBase):
    """
    Animate a single pixel
    """
    colors: list
    color_idx: int

    def __init__(self, pos: Vector2D, colors: list):
        """
        :param pos: Position of the pixel to animate
        :param colors: Colors of the pixel, colors do loop
        """
        super().__init__(pos)
        self.colors = colors

        self.color_idx = 0

    def render(self, renderer: RendererBase):
        """
        renders next frame

        :param renderer: renderer on which to display the pixel
        """
        renderer.set_led(self.position.x, self.position.y, self.colors[self.color_idx])
        self.color_idx = self.color_idx + 1 if self.color_idx < len(self.colors) - 1 else 0

from core.rendering.animations.AnimatedPixel import AnimatedPixel
from core.rendering.animations.AnimationBase import AnimationBase
from core.rendering.renderer.RendererBase import RendererBase
from core.util.Vector2D import Vector2D


class AnimatedCluster(AnimationBase):
    pixels: []
    colors: []
    rel_coordinates: [Vector2D]

    def __setattr__(self, key, value):
        # only overrides accessing position, to apply changes
        # default operation, when argument is not position
        if key != 'position':
            super().__setattr__(key, value)
            return

        # if position exists; this is not the fist access, change the position of every pixel
        if hasattr(self, key):
            for px, cord in zip(self.pixels, self.rel_coordinates):
                px.position = cord + value
        super().__setattr__(key, value)

    def __init__(self, pos: Vector2D, colors: list, relative_coordinates: [Vector2D]):
        """
        Animate multiple pixels at once

        :param pos: starting position
        :param colors: colors which each pixel has in one frame
        :param relative_coordinates: relative coordinates for each pixel
        """
        super().__init__(pos)
        self.colors = colors
        self.rel_coordinates = relative_coordinates
        self.pixels = []

        # generates animated pixels
        for cord in self.rel_coordinates:
            self.pixels.append(AnimatedPixel(pos=self.position + cord, colors=self.colors))

    def render(self, renderer: RendererBase):
        """
        renders next frame

        :param renderer: renderer on which to display the pixel
        """
        for px in self.pixels:
            px.render(renderer)

from PIL import Image

from core.rendering.animations.AnimationBase import AnimationBase
from core.rendering.renderer.RendererBase import RendererBase


class GifRenderer(AnimationBase):
    index: int
    gif: any

    def __init__(self, file_path: str, pos):
        super().__init__(pos)
        self.gif = Image.open(file_path)
        self.index = 1

    def render(self, renderer: RendererBase):
        """
        renders next frame

        :param renderer: renderer on which to display the pixel
        """
        self.gif.seek(self.index)
        img = self.gif
        for x in range(renderer.screen.size_x):
            for y in range(renderer.screen.size_y):
                color = img.getpixel((x, renderer.screen.size_y-1-y))
                renderer.set_led(x + self.position.x, y + self.position.y, color)

        self.index = self.index + 1 if self.index + 1 < self.gif.n_frames else 1

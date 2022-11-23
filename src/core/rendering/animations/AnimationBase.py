import time

from core.rendering.renderer.RendererBase import RendererBase
from core.util.Vector2D import Vector2D


class AnimationBase:
    position: Vector2D

    def __init__(self, pos):
        self.position = pos

    def render(self, renderer: RendererBase):
        pass

    # TODO: add continues running thread for render

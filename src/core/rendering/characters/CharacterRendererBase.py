from core.util.Vector2D import Vector2D
from core.rendering.renderer.RendererBase import RendererBase


class CharacterRendererBase:
    pos: Vector2D
    size: Vector2D

    def __init__(self, pos: Vector2D):
        """
        :param pos: Starting Position, the lower left corner
        """
        if self.pos:
            if int(self.pos.x) != self.pos.x or int(self.pos.y) != self.pos.y:
                raise ValueError("Position Vector must only contain integer numbers")
            self.pos = pos

    def render(self, characters, renderer: RendererBase):
        pass

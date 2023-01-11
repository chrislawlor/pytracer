import math
from dataclasses import dataclass, field

from .color import Color
from .matrix import Matrix
from .primitives import Point


@dataclass()
class Pattern:
    colors: list[Color]
    transform: Matrix = field(default_factory=lambda: Matrix.identity(4))

    @classmethod
    def stripes(cls, color_1: Color, color_2: Color):
        return cls(colors=[color_1, color_2])

    def color_at_local_transform(self, transform: Matrix, world_point: Point) -> Color:
        object_point = transform.inverse() * world_point
        pattern_point = self.transform.inverse() * object_point
        return self.color_at_world_coords(pattern_point)

    def color_at_world_coords(self, at: Point) -> Color:
        idx = math.floor(at.x % len(self.colors))
        return self.colors[idx]

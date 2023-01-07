from dataclasses import dataclass, field

from .color import Color
from .primitives import Point


@dataclass(slots=True)
class PointLight:
    position: Point
    intensity: Color = field(default_factory=lambda: Color(1, 1, 1))

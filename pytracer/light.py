from dataclasses import dataclass

from .color import Color
from .primitives import Point


@dataclass(slots=True)
class PointLight:
    position: Point
    intensity: Color

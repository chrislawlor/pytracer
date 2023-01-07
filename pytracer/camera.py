import math
from dataclasses import dataclass, field
from typing import Optional

from .canvas import Canvas
from .matrix import Matrix
from .primitives import Point
from .ray import Ray
from .world import World


@dataclass
class Camera:
    hsize: int = 160
    vsize: int = 120
    field_of_view: float = math.pi / 2
    transform: Matrix = field(default_factory=lambda: Matrix.identity(4))

    def render(self, world: World):
        image = Canvas(self.hsize, self.vsize)

        for y in range(self.vsize):
            for x in range(self.hsize):
                ray = self.ray_for_pixel(x, y)
                color = world.color_at(ray)
                image.write_pixel(x, y, color)
        return image

    def __post_init__(self):
        self._half_height: Optional[float] = None
        self._half_width: Optional[float] = None
        self._pixel_size: Optional[float] = None

    @property
    def pixel_size(self):
        if self._pixel_size is None:
            self._compute_properties()
        return self._pixel_size

    @property
    def half_width(self):
        if self._half_width is None:
            self._compute_properties
        return self._half_width

    @property
    def half_heigth(self):
        if self._half_height is None:
            self._compute_properties
        return self._half_height

    def ray_for_pixel(self, px, py) -> Ray:
        xoffset = (px + 0.5) * self.pixel_size
        yoffset = (py + 0.5) * self.pixel_size

        # calculate the untransformed coords in world space,
        # remembering that the camera points toward -z
        # so +x is to the *left*
        world_x = self.half_width - xoffset
        world_y = self.half_heigth - yoffset

        # using the camera matrix, transform the canvas point
        # and the origin, and then compute the ray's direction
        # vector
        # (remember that the canvas is at z=-1)
        inverse_xform = self.transform.inverse()
        pixel = inverse_xform * Point(world_x, world_y, -1)
        origin = inverse_xform * Point(0, 0, 0)
        direction = (pixel - origin).normalize()
        return Ray(origin, direction)

    def _compute_properties(self):
        half_view = math.tan(self.field_of_view / 2)
        aspect = self.hsize / self.vsize

        if aspect >= 1:
            self._half_width = half_view
            self._half_height = half_view / aspect
        else:
            self._half_width = half_view * aspect
            self._half_height = half_view

        self._pixel_size = self._half_width * 2 / self.hsize

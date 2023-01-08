from __future__ import annotations

from dataclasses import dataclass, field

from .color import Color
from .light import PointLight
from .matrix import Matrix
from .primitives import Point, Vector3
from .ray import Intersection, Ray
from .sphere import Sphere
from .utils import EPSILON


@dataclass
class World:
    shapes: list[Sphere] = field(default_factory=list)
    lights: list[PointLight] = field(default_factory=list)

    def color_at(self, ray) -> Color:
        intersections = self.intersect(ray)
        hit = Intersection.hit(intersections)
        if hit is None:
            return Color(0, 0, 0)
        comps = self.prepare_computations(hit, ray)
        return self.shade_hit(comps)

    def is_shadowed(self, point: Point, light: PointLight) -> bool:
        v = light.position - point
        distance = v.magnitude
        direction = v.normalize()

        r = Ray(point, direction)
        intersections = self.intersect(r)
        h = Intersection.hit(intersections)
        if h and h.t < distance:
            return True
        return False

    def intersect(self, ray: Ray) -> list[Intersection]:
        """Returns list of Intersections sorted by t"""
        intersections = []
        for sphere in self.shapes:
            intersections += ray.intersects(sphere)
        intersections.sort(key=lambda i: i.t)
        return intersections

    @staticmethod
    def prepare_computations(intersection: Intersection, ray: Ray) -> Comps:
        position = ray.position(intersection.t)
        eyev = -ray.direction
        normalv = intersection.shape.normal_at(position)
        inside = False

        if normalv.dot(eyev) < 0:
            inside = True
            normalv = -normalv
        return Comps(
            t=intersection.t,
            shape=intersection.shape,
            position=position,
            over_point=position + normalv * EPSILON,
            eyev=eyev,
            normalv=normalv,
            inside=inside,
        )

    def shade_hit(self, comps: Comps):
        """Computes color for each light and return the sum"""
        color = Color(0, 0, 0)
        for light in self.lights:
            is_shadowed = self.is_shadowed(comps.over_point, light)

            color += comps.shape.material.lighting(
                light, comps.position, comps.eyev, comps.normalv, in_shadow=is_shadowed
            )

        return color

    @classmethod
    def view_transform(cls, from_: Point, to: Point, up: Vector3):
        forward = (to - from_).normalize()
        up = up.normalize()
        left = forward.cross_product(up)
        true_up = left.cross_product(forward)
        orientation = Matrix(
            [
                [left.x, left.y, left.z, 0],
                [true_up.x, true_up.y, true_up.z, 0],
                [-forward.x, -forward.y, -forward.z, 0],
                [0, 0, 0, 1],
            ]
        )
        return orientation * Matrix.translation(-from_.x, -from_.y, -from_.z)


@dataclass(slots=True)
class Comps:
    t: float
    shape: Sphere
    position: Point
    over_point: Point
    eyev: Vector3
    normalv: Vector3
    inside: bool = False

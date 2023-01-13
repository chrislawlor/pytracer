from __future__ import annotations

from dataclasses import dataclass, field

from .color import Color
from .light import PointLight
from .matrix import Matrix
from .primitives import Point, Vector3
from .ray import Intersection, Ray
from .shapes import Shape
from .utils import EPSILON

MAX_REFLECTIONS = 5


@dataclass
class World:
    shapes: list[Shape] = field(default_factory=list)
    lights: list[PointLight] = field(default_factory=list)

    def color_at(self, ray, remaining=MAX_REFLECTIONS) -> Color:
        if remaining == 0:
            return Color(0, 0, 0)
        intersections = self.intersect(ray)
        hit = Intersection.hit(intersections)
        if hit is None:
            return Color(0, 0, 0)
        comps = self.prepare_computations(hit, ray)
        return self.shade_hit(comps, remaining=remaining)

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
            reflectv=ray.direction.reflect(normalv),
            inside=inside,
        )

    def shade_hit(self, comps: Comps, remaining=MAX_REFLECTIONS) -> Color:
        """Computes color for each light and return the sum"""
        color = Color(0, 0, 0)
        for light in self.lights:
            is_shadowed = self.is_shadowed(comps.over_point, light)

            color += comps.shape.material.lighting(
                light,
                comps.position,
                comps.eyev,
                comps.normalv,
                in_shadow=is_shadowed,
                local_transform=comps.shape.transform,
            )

            color += self.reflected_color(comps, remaining=remaining)

        return color

    def reflected_color(self, comps: Comps, remaining=MAX_REFLECTIONS) -> Color:
        if comps.shape.material.reflective == 0:
            return Color(0, 0, 0)

        reflect_ray = Ray(comps.over_point, comps.reflectv)
        color = self.color_at(reflect_ray, remaining=remaining - 1)
        return color * comps.shape.material.reflective

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
    shape: Shape
    position: Point
    over_point: Point
    eyev: Vector3
    normalv: Vector3
    reflectv: Vector3
    inside: bool = False

from __future__ import annotations

from dataclasses import dataclass, field

from .color import Color
from .light import PointLight
from .primitives import Point, Vector3
from .ray import Intersection, Ray
from .sphere import Sphere


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
            eyev=eyev,
            normalv=normalv,
            inside=inside,
        )

    def shade_hit(self, comps: Comps):
        """Computes color for each light and return the sum"""
        color = Color(0, 0, 0)
        for light in self.lights:
            color += comps.shape.material.lighting(
                light, comps.position, comps.eyev, comps.normalv
            )

        return color


@dataclass(slots=True)
class Comps:
    t: float
    shape: Sphere
    position: Point
    eyev: Vector3
    normalv: Vector3
    inside: bool = False

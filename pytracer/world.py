from __future__ import annotations

from dataclasses import dataclass, field

from .color import Color
from .light import PointLight
from .materials import Material
from .matrix import Matrix
from .primitives import Point, Vector3
from .ray import Intersection, Ray
from .sphere import Sphere


@dataclass
class World:
    shapes: list[Sphere] = field(default_factory=list)
    lights: list[PointLight] = field(default_factory=list)

    @classmethod
    def default(cls) -> World:
        return cls(shapes=cls._default_shapes(), lights=[cls._default_light()])

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

    @classmethod
    def _default_shapes(cls) -> list[Sphere]:
        s1 = Sphere()
        s1.material = Material(
            color=Color(0.8, 1.0, 0.6),
            ambient=0.1,
            diffuse=0.7,
            specular=0.2,
            shininess=50,
        )
        s2 = Sphere()
        s2.material = Material(
            color=Color(1, 1, 1), ambient=0.1, diffuse=0.9, specular=0.9, shininess=200
        )
        s2.transform = Matrix.scaling(0.5, 0.5, 0.5)
        return [s1, s2]

    @classmethod
    def _default_light(cls) -> PointLight:
        return PointLight(position=Point(-10, 10, -10), intensity=Color(1, 1, 1))


@dataclass(slots=True)
class Comps:
    t: float
    shape: Sphere
    position: Point
    eyev: Vector3
    normalv: Vector3
    inside: bool = False

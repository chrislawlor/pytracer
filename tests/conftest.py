from copy import copy

import pytest

from pytracer import Color, Material, Matrix, Point, PointLight, Sphere, World


@pytest.fixture
def material():
    return Material(
        color=Color(1, 1, 1), ambient=0.1, diffuse=0.9, specular=0.9, shininess=200
    )


@pytest.fixture
def sphere(material):
    return Sphere(material=material)


@pytest.fixture
def world(sphere):
    s1 = sphere
    s2 = copy(s1)

    s1.material = Material(
        color=Color(0.8, 1.0, 0.6), ambient=0.1, diffuse=0.7, specular=0.2, shininess=50
    )
    s2.transform = Matrix.scaling(0.5, 0.5, 0.5)

    light = PointLight(position=Point(-10, 10, -10), intensity=Color(1, 1, 1))
    return World(shapes=[s1, s2], lights=[light])

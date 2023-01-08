import pytest

from pytracer.shapes import Plane, Point, Ray, Vector3


@pytest.mark.parametrize(
    ("point",),
    (
        (Point(0, 0, 0),),
        (Point(10, 0, -10),),
        (Point(-5, 0, 150),),
    ),
)
def test_normal_is_constant(point: Point):
    p = Plane()
    assert p.normal_at(point) == Vector3(0, 1, 0)


def test_intersect_with_ray_parallel_to_the_plane():
    p = Plane()
    r = Ray(Point(0, 10, 0), Vector3(0, 0, 1))
    assert p.local_intersect(r) == []


def test_intersect_with_coplaner_ray():
    p = Plane()
    r = Ray(Point(0, 0, 0), Vector3(0, 0, 1))
    assert p.local_intersect(r) == []


def test_ray_intersecting_a_plane_from_above():
    p = Plane()
    r = Ray(Point(0, 1, 0), Vector3(0, -1, 0))

    xs = p.local_intersect(r)

    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].shape == p


def test_ray_intersecting_a_plane_from_below():
    p = Plane()
    r = Ray(Point(0, -1, 0), Vector3(0, 1, 0))

    xs = p.local_intersect(r)

    assert len(xs) == 1
    assert xs[0].t == 1
    assert xs[0].shape == p

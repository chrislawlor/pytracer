from math import pi, sqrt

from pytracer import Camera, Color, Matrix, Point, Vector3, World

from .utils import approx


def test_camera_defaults():
    # becuase change in defaults can break tests,
    # this records what the tests expect the defaults
    # to be.
    c = Camera()
    assert c.hsize == 160
    assert c.vsize == 120
    assert c.field_of_view == pi / 2
    assert c.transform == Matrix.identity(4)


def test_pixel_size_for_landscape_canvas():
    c = Camera(hsize=200, vsize=125)
    assert c.pixel_size == approx(0.01)


def test_pixel_size_for_portrait_canvas():
    c = Camera(hsize=125, vsize=200)
    assert c.pixel_size == approx(0.01)


def test_construct_a_ray_through_the_center_of_the_canvas():
    c = Camera(201, 101)

    r = c.ray_for_pixel(100, 50)

    assert r.origin == Point(0, 0, 0)
    assert r.direction == Vector3(0, 0, -1)


def test_construct_a_ray_to_the_corner_of_the_canvas():
    c = Camera(201, 101)

    r = c.ray_for_pixel(0, 0)

    assert r.origin == Point(0, 0, 0)
    assert r.direction == Vector3(0.66519, 0.33259, -0.66851)


def test_construct_a_ray_when_the_camera_is_transformed():
    c = Camera(201, 101)
    c.transform = Matrix.rotation_y(pi / 4) * Matrix.translation(0, -2, 5)

    r = c.ray_for_pixel(100, 50)

    assert r.origin == Point(0, 2, -5)
    assert r.direction == Vector3(sqrt(2) / 2, 0, -sqrt(2) / 2)


def test_rendering_a_world(world):
    c = Camera(11, 11, pi / 2)
    c.transform = World.view_transform(
        from_=Point(0, 0, -5), to=Point(0, 0, 0), up=Vector3(0, 1, 0)
    )
    image = c.render(world)
    assert image.pixel_at(5, 5) == Color(0.38066, 0.47583, 0.2855)

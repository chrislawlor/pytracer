from math import pi, sqrt

from pytracer import Matrix, Point, Sphere, Vector3


def test_the_normal_on_a_sphere_at_a_point_on_x_axis():
    s = Sphere()
    n = s.normal_at(Point(1, 0, 0))
    assert n == Vector3(1, 0, 0)


def test_the_normal_on_a_sphere_at_a_point_on_y_axis():
    s = Sphere()
    n = s.normal_at(Point(0, 1, 0))
    assert n == Vector3(0, 1, 0)


def test_the_normal_on_a_sphere_at_a_point_on_z_axis():
    s = Sphere()
    n = s.normal_at(Point(0, 0, 1))
    assert n == Vector3(0, 0, 1)


def test_the_normal_on_a_sphere_at_a_non_axial_point():
    s = Sphere()
    v = sqrt(3) / 3
    n = s.normal_at(Point(v, v, v))
    assert n == Vector3(v, v, v)
    assert n == Vector3(v, v, v)


def test_the_normal_is_a_normalized_vector():
    s = Sphere()
    v = sqrt(3) / 3
    n = s.normal_at(Point(v, v, v))
    assert n == n.normalize()


def test_computing_the_normal_on_a_translated_sphere():
    s = Sphere()
    s.transform = Matrix.translation(0, 1, 0)
    n = s.normal_at(Point(0, 1.70711, -0.70711))
    assert n == Vector3(0, 0.70711, -0.70711)


def test_computing_the_normal_on_a_transformed_sphere():
    s = Sphere()
    s.transform = Matrix.scaling(1, 0.5, 1) * Matrix.rotation_z(pi / 5)
    n = s.normal_at(Point(0, sqrt(2) / 2, -sqrt(2) / 2))
    assert n == Vector3(0, 0.970143, -0.242536)

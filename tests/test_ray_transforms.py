from pytracer import Matrix, Point, Ray, Vector3


def test_translating_a_ray():
    r = Ray(Point(1, 2, 3), Vector3(0, 1, 0))
    m = Matrix.translation(3, 4, 5)
    r2 = r.transform(m)
    assert r2.origin == Point(4, 6, 8)
    assert r2.direction == Vector3(0, 1, 0)


def test_scaling_a_ray():
    r = Ray(Point(1, 2, 3), Vector3(0, 1, 0))
    m = Matrix.scaling(2, 3, 4)
    r2 = r.transform(m)
    assert r2.origin == Point(2, 6, 12)
    assert r2.direction == Vector3(0, 3, 0)

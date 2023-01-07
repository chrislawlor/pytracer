from pytracer import Color, Intersection, Point, PointLight, Ray, Sphere, Vector3, World


def test_intersect_world_with_ray():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))

    xs = w.intersect(r)

    assert len(xs) == 4
    assert xs[0].t == 4
    assert xs[1].t == 4.5
    assert xs[2].t == 5.5
    assert xs[3].t == 6


def test_precomputing_the_state_of_an_intersection():
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)

    comps = World.prepare_computations(i, r)

    assert comps.t == i.t
    assert comps.shape == i.shape
    assert comps.position == Point(0, 0, -1)
    assert comps.eyev == Vector3(0, 0, -1)
    assert comps.normalv == Vector3(0, 0, -1)


def test_the_hit_when_x_occurs_on_the_outside():
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)

    comps = World.prepare_computations(i, r)

    assert comps.inside is False


def test_the_hit_when_x_occurs_on_the_inside():
    r = Ray(Point(0, 0, 0), Vector3(0, 0, 1))
    shape = Sphere()
    i = Intersection(1, shape)

    comps = World.prepare_computations(i, r)

    assert comps.position == Point(0, 0, 1)
    assert comps.eyev == Vector3(0, 0, -1)
    assert comps.inside is True
    assert comps.normalv == Vector3(0, 0, -1)


def test_shading_an_intersection():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
    shape = w.shapes[0]
    i = Intersection(4, shape)

    comps = w.prepare_computations(i, r)
    color = w.shade_hit(comps)

    assert color == Color(0.38066, 0.47583, 0.2855)


def test_shading_an_intersection_from_the_inside():
    w = World.default()
    w.lights = [PointLight(Point(0, 0.25, 0), Color(1, 1, 1))]
    r = Ray(Point(0, 0, 0), Vector3(0, 0, 1))
    shape = w.shapes[1]
    i = Intersection(0.5, shape)

    comps = w.prepare_computations(i, r)
    color = w.shade_hit(comps)

    assert color == Color(0.90498, 0.90498, 0.90498)


def test_color_when_ray_misses():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector3(0, 1, 0))

    color = w.color_at(r)

    assert color == Color(0, 0, 0)


def test_color_when_ray_hits():
    w = World.default()
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))

    color = w.color_at(r)

    assert color == Color(0.38066, 0.47583, 0.2855)


def test_color_with_an_intersection_behind_the_ray():
    w = World.default()
    outer = w.shapes[0]
    outer.material.ambient = 1
    inner = w.shapes[1]
    inner.material.ambient = 1
    r = Ray(Point(0, 0, 0.75), Vector3(0, 0, -1))

    color = w.color_at(r)

    assert color == inner.material.color

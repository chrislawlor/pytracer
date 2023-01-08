from copy import copy

from pytracer import (
    Color,
    Intersection,
    Matrix,
    Point,
    PointLight,
    Ray,
    Sphere,
    Vector3,
    World,
)

from .utils import assert_matrix_approx_equal


def test_intersect_world_with_ray(world: World):
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))

    xs = world.intersect(r)

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


def test_shading_an_intersection(world: World):
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
    shape = world.shapes[0]
    i = Intersection(4, shape)

    comps = world.prepare_computations(i, r)
    color = world.shade_hit(comps)

    assert color == Color(0.38066, 0.47583, 0.2855)


def test_shading_an_intersection_from_the_inside(world):
    world.lights = [PointLight(Point(0, 0.25, 0), Color(1, 1, 1))]
    r = Ray(Point(0, 0, 0), Vector3(0, 0, 1))
    shape = world.shapes[1]
    i = Intersection(0.5, shape)

    comps = world.prepare_computations(i, r)
    color = world.shade_hit(comps)

    assert color == Color(0.90498, 0.90498, 0.90498)


def test_color_when_ray_misses(world: World):
    r = Ray(Point(0, 0, -5), Vector3(0, 1, 0))

    color = world.color_at(r)

    assert color == Color(0, 0, 0)


def test_color_when_ray_hits(world):
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))

    color = world.color_at(r)

    assert color == Color(0.38066, 0.47583, 0.2855)


def test_color_with_an_intersection_behind_the_ray(world):
    outer = world.shapes[0]
    outer.material.ambient = 1
    inner = world.shapes[1]
    inner.material.ambient = 1
    r = Ray(Point(0, 0, 0.75), Vector3(0, 0, -1))

    color = world.color_at(r)

    assert color == inner.material.color


def test_transformation_matrix_for_default_orientation():
    from_ = Point(0, 0, 0)
    to = Point(0, 0, -1)
    up = Vector3(0, 1, 0)

    t = World.view_transform(from_, to, up)

    assert t == Matrix.identity(4)


def test_view_transform_looking_in_positive_z_direction():
    from_ = Point(0, 0, 0)
    to = Point(0, 0, 1)
    up = Vector3(0, 1, 0)

    t = World.view_transform(from_, to, up)

    assert t == Matrix.scaling(-1, 1, -1)


def test_view_transform_moves_the_world():
    from_ = Point(0, 0, 8)
    to = Point(0, 0, 0)
    up = Vector3(0, 1, 0)

    t = World.view_transform(from_, to, up)

    assert t == Matrix.translation(0, 0, -8)


def test_an_arbitrary_view_transformation():
    from_ = Point(1, 3, 2)
    to = Point(4, -2, 8)
    up = Vector3(1, 1, 0)

    t = World.view_transform(from_, to, up)

    expected = Matrix(
        [
            # fmt: off
        [-0.50709, 0.50709,  0.67612, -2.36643],
        [ 0.76772, 0.60609,  0.12122, -2.82843],
        [-0.35857, 0.59761, -0.71714,  0.00000],
        [ 0.00000, 0.00000,  0.00000,  1.00000]
            # fmt: on
        ]
    )
    assert_matrix_approx_equal(t, expected)
    assert_matrix_approx_equal(t, expected)


def test_no_shadow_when_nothing_is_collinear_between_point_and_light(world: World):
    p = Point(0, 10, 0)
    assert world.is_shadowed(p, world.lights[0]) is False


def test_shadowed_when_obj_is_between_point_and_light(world: World):
    p = Point(10, -10, 10)
    assert world.is_shadowed(p, world.lights[0]) is True


def test_no_shadow_when_obj_is_behind_the_light(world: World):
    p = Point(-20, 20, -20)
    assert world.is_shadowed(p, world.lights[0]) is False


def test_no_shadow_when_obj_is_behind_the_point(world: World):
    p = Point(-2, 2, -2)
    assert world.is_shadowed(p, world.lights[0]) is False


def test_shade_hit_given_an_intersection_in_shadow(world: World):
    world.lights = [PointLight(Point(0, 0, -10))]

    s1 = world.shapes[0]
    s2 = copy(s1)
    s2.material.color = Color(1, 1, 1)
    s2.transform = Matrix.translation(0, 0, 10)
    world.shapes.append(s2)
    r = Ray(Point(0, 0, 5), Vector3(0, 0, 1))
    i = Intersection(4, s2)
    comps = world.prepare_computations(i, r)
    color = world.shade_hit(comps)
    assert color == Color(0.1, 0.1, 0.1)

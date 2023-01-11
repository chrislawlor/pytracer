from math import sqrt

from pytracer import Color, Material, Pattern, Point, PointLight, Vector3


def test_lighting_with_the_eye_between_the_light_and_surface(material: Material):
    # Eye is positioned directly between the light and the
    # surface, with the normal pointing directly at the eye,
    # maximizing the effect of ambient, diffuse, and specular
    # values.
    position = Point(0, 0, 0)
    eyev = Vector3(0, 0, -1)
    normalv = Vector3(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))

    result = material.lighting(light, position, eye_vector=eyev, normal_vector=normalv)

    expected_color_val = material.ambient + material.diffuse + material.specular

    assert result == Color(expected_color_val, expected_color_val, expected_color_val)


def test_lighting_eye_between_light_and_surface_45_deg(material: Material):
    # Same as above, but eye is at a 45 degree angle, nullifying specular
    position = Point(0, 0, 0)
    eyev = Vector3(0, sqrt(2) / 2, -sqrt(2) / 2)
    normalv = Vector3(0, 0, -1)
    light = PointLight(Point(0, 0, -10), Color(1, 1, 1))

    result = material.lighting(light, position, eye_vector=eyev, normal_vector=normalv)

    expected_color_val = material.ambient + material.diffuse

    assert result == Color(expected_color_val, expected_color_val, expected_color_val)


def test_normal_points_at_eye_but_light_at_45_deg(material: Material):
    # diffuse becomes material.diffuse * Sqrt(2) / 2, specular 0
    position = Point(0, 0, 0)
    eyev = Vector3(0, 0, -1)
    normalv = Vector3(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))

    result = material.lighting(light, position, eye_vector=eyev, normal_vector=normalv)

    expected_color_val = material.ambient + material.diffuse * sqrt(2) / 2

    assert result == Color(expected_color_val, expected_color_val, expected_color_val)


def test_eye_directly_in_path_of_reflection_vector(material: Material):
    # specular becomes full strength
    position = Point(0, 0, 0)
    eyev = Vector3(0, -sqrt(2) / 2, -sqrt(2) / 2)
    normalv = Vector3(0, 0, -1)
    light = PointLight(Point(0, 10, -10), Color(1, 1, 1))

    result = material.lighting(light, position, eye_vector=eyev, normal_vector=normalv)

    expected_color_val = (
        material.ambient + material.diffuse * sqrt(2) / 2 + material.specular
    )

    assert result == Color(expected_color_val, expected_color_val, expected_color_val)


def test_light_behind_material(material: Material):
    # total intensity is just the ambient component
    position = Point(0, 0, 0)
    eyev = Vector3(0, 0, -1)
    normalv = Vector3(0, 0, -1)
    light = PointLight(Point(0, 0, 10), Color(1, 1, 1))

    result = material.lighting(light, position, eye_vector=eyev, normal_vector=normalv)

    expected_color_val = material.ambient

    assert result == Color(expected_color_val, expected_color_val, expected_color_val)


def test_lighting_with_the_surface_in_shadow(material: Material):
    position = Point(0, 0, 0)
    eyev = Vector3(0, 0, -1)
    normalv = Vector3(0, 0, -1)
    light = PointLight(Point(0, 0, -10))

    result = material.lighting(light, position, eyev, normalv, in_shadow=True)

    assert result == Color(0.1, 0.1, 0.1)


def test_lighting_with_a_pattern_applied():
    WHITE = Color(1, 1, 1)
    BLACK = Color(0, 0, 0)
    pattern = Pattern.stripes(WHITE, BLACK)
    material = Material(
        ambient=1, diffuse=0, specular=0, pattern=pattern, color=WHITE, shininess=50
    )
    eyev = Vector3(0, 0, -1)
    normalv = Vector3(0, 0, -1)
    light = PointLight(Point(0, 0, -10))

    c1 = material.lighting(light, Point(0.9, 0, 0), eyev, normalv)
    c2 = material.lighting(light, Point(1.1, 0, 0), eyev, normalv)

    assert c1 == WHITE
    assert c2 == BLACK

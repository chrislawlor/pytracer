from math import pi
from textwrap import dedent

import pytest

from pytracer import Color, Material, Matrix
from pytracer.serialization import (
    load_colors,
    load_materials,
    load_shapes,
    load_transforms,
    load_yaml,
)


def test_load_color_hex():
    d = {"test": {"hex": "ffffff"}}

    colors = load_colors(d)

    assert "test" in colors
    assert colors["test"] == Color(1, 1, 1)


def test_load_color_rgb():
    d = {"test": {"rgb": [0, 255, 0]}}

    colors = load_colors(d)

    assert "test" in colors
    assert colors["test"] == Color(0, 1, 0)


def test_invalid_color_spec():
    d = {"test": {"wrong": "stuff"}}
    with pytest.raises(ValueError):
        load_colors(d)


def test_load_material_with_named_color():
    colors = {"testColor": Color(1, 1, 1)}
    spec = {
        "testMat": {
            "color": "testColor",
            "ambient": 0.1,
            "diffuse": 0.9,
            "specular": 0.9,
            "shininess": 100,
        }
    }

    mats = load_materials(spec, colors)

    assert "testMat" in mats
    assert mats["testMat"].color == Color(1, 1, 1)


def test_material_with_inline_color_spec():
    spec = {
        "testMat": {
            "color": {"hex": "ffffff"},
            "ambient": 0.1,
            "diffuse": 0.9,
            "specular": 0.9,
            "shininess": 100,
        }
    }

    mats = load_materials(spec, {})

    assert "testMat" in mats
    assert mats["testMat"].color == Color(1, 1, 1)


def test_material_with_undefined_color_name():
    spec = {
        "testMat": {
            "color": "testColor",
            "ambient": 0.1,
            "diffuse": 0.9,
            "specular": 0.9,
            "shininess": 100,
        }
    }

    with pytest.raises(ValueError):
        load_materials(spec, {})


def test_empty_transform_is_identity():
    assert load_transforms([]) == Matrix.identity(4)


@pytest.mark.parametrize(
    ("spec", "expected"),
    (
        ({"scaling": [2, 2, 2]}, Matrix.scaling(2, 2, 2)),
        ({"rotation_x": "pi/2"}, Matrix.rotation_x(pi / 2)),
        ({"rotation_y": "pi/4"}, Matrix.rotation_y(pi / 4)),
        ({"rotation_z": "pi/2"}, Matrix.rotation_z(pi / 2)),
        ({"translation": [1, 2, 3]}, Matrix.translation(1, 2, 3)),
        ({"shearing": [1, 2, 3, 4, 5, 6]}, Matrix.shearing(1, 2, 3, 4, 5, 6)),
    ),
)
def test_single_transform(spec, expected):
    transform = load_transforms([spec])

    assert transform == expected


def test_transform_with_pi():
    transforms = [{"rotation_x": "pi/2"}]

    transform = load_transforms(transforms)

    assert transform == Matrix.rotation_x(pi / 2)

    assert transform == Matrix.rotation_x(pi / 2)
    assert transform == Matrix.rotation_x(pi / 2)


def test_transforms_applied_in_correct_order():
    transforms = [{"scaling": [1, 2, 1]}, {"rotation_z": "pi/2"}]

    transform = load_transforms(transforms)

    expected = Matrix.rotation_z(pi / 2) * Matrix.scaling(1, 2, 1)

    assert transform == expected


def test_load_shape_with_named_material(material):
    materials = {"floor": material}

    spec = [{"sphere": {"material": "floor"}}]

    shapes = load_shapes(spec, materials, {})

    assert len(shapes) == 1
    assert shapes[0].material == material
    assert shapes[0].transform == Matrix.identity(4)


def test_load_shape_with_inline_material():
    spec = [
        {
            "sphere": {
                "material": {
                    "color": {"hex": "ffffff"},
                    "ambient": 0.1,
                    "diffuse": 0.9,
                    "specular": 0.9,
                    "shininess": 50,
                }
            }
        }
    ]

    shapes = load_shapes(spec, {}, {})

    assert len(shapes) == 1
    assert shapes[0].material == Material(
        color=Color(1, 1, 1), ambient=0.1, diffuse=0.9, specular=0.9, shininess=50
    )


SCENE_FILE = dedent(
    """
    camera:
      hsize: 200
      vsize: 100
      field_of_view: "pi/2"
      view_transform:
        from: [0, 1.5, -5]
        to: [0, 1, 0]
        up: [0, 1, 0]

    colors:
      robinEggBlue:
        hex: 81d8d0

    materials:
      robinEgg:
          color: robinEggBlue
          ambient: 0.1
          diffuse: 0.9
          specular: 0.8
          shininess: 80
      grass:
        color:
          rgb: [63, 158, 4]
        ambient: 0.2
        diffuse: 0.9
        specular: 0.5
        shininess: 50

    shapes:
      - sphere:
          material: robinEgg
          transforms:
            - scaling: [2, 2, 2]
            - translation: [0, 2, 0]
      - plane:
          material: grass

    lights:
      - position: [5, 5, 5]
        color:
          rgb: [255, 250, 250]

    """
)


def test_load_scene():
    camera, world = load_yaml(SCENE_FILE)

    assert camera.hsize == 200
    assert camera.vsize == 100
    assert len(world.shapes) == 2
    assert world.shapes[0].material.color == Color(
        red=0.50588, green=0.84705, blue=0.81568
    )
    assert len(world.lights) == 1

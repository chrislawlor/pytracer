import operator
from functools import reduce
from math import pi
from typing import Any, Union

import yaml as pyyaml

from .camera import Camera
from .color import Color
from .light import PointLight
from .materials import Material
from .matrix import Matrix
from .primitives import Point, Vector3
from .shapes import Plane, Shape, Sphere
from .world import World


def load_yaml(yaml: str) -> tuple[Camera, World]:
    return load(pyyaml.load(yaml, pyyaml.Loader))


def load(world_dict: dict[str, Any]) -> tuple[Camera, World]:
    colors = load_colors(world_dict.get("colors", {}))
    materials = load_materials(world_dict.get("materials", {}), colors)
    shapes = load_shapes(world_dict.get("shapes", []), materials, colors)
    lights = load_lights(world_dict.get("lights", []), colors)
    world = World(shapes=shapes, lights=lights)
    camera = load_camera(world_dict["camera"], world)
    return camera, world


def load_color(colorspec) -> Color:
    if "hex" in colorspec:
        return Color.from_hex(colorspec["hex"])
    if "rgb" in colorspec:
        try:
            rgb = colorspec["rgb"]
            r, g, b = rgb
            return Color.from_rgb(r, g, b)
        except ValueError as e:
            raise ValueError(
                f"Wrong number of color arguments. Expected 3, got {len(rgb)}: {rgb}"
            ) from e
    raise ValueError(f"Invalid color spec: {colorspec}")


def load_colors(colorsdict) -> dict[str, Color]:
    colors: dict[str, Color] = {}
    for name, spec in colorsdict.items():
        colors[name] = load_color(spec)
    return colors


def load_material(spec, colors: dict[str, Color]) -> Material:
    try:
        color_spec = spec["color"]
        if isinstance(color_spec, str):
            if color_spec not in colors:
                raise ValueError(f"Undefined color name: {color_spec}")
            color = colors[color_spec]
        else:
            color = load_color(color_spec)
        spec["color"] = color
        return Material(**spec)

    except KeyError as e:
        raise ValueError("Invalid material specification") from e


def load_materials(materialsdict, colors: dict[str, Color]) -> dict[str, Material]:
    materials: dict[str, Material] = {}
    for name, spec in materialsdict.items():
        materials[name] = load_material(spec, colors)
    return materials


def p(val):
    """
    Support use of "pi" in values, e.g. "rotation_x: pi / 2"
    """
    if isinstance(val, str):
        return eval(val, {"pi": pi, "__builtins__": {}})
    return val


def load_transforms(transforms: list[dict]) -> Matrix:
    # File format list transforms in semantic order, but
    # our transforms must be applied in reverse

    xforms = []

    for xform in transforms:
        match xform:
            case {"scaling": [x, y, z]}:
                xforms.append(Matrix.scaling(p(x), p(y), p(z)))
            case {"rotation_x": x}:
                xforms.append(Matrix.rotation_x(p(x)))
            case {"rotation_y": y}:
                xforms.append(Matrix.rotation_y(p(y)))
            case {"rotation_z": z}:
                xforms.append(Matrix.rotation_z(p(z)))
            case {"shearing": [Xy, Xz, Yx, Yz, Zx, Zy]}:
                xforms.append(Matrix.shearing(p(Xy), p(Xz), p(Yx), p(Yz), p(Zx), p(Zy)))
            case {"translation": [x, y, z]}:
                xforms.append(Matrix.translation(p(x), p(y), p(z)))
            case _:
                raise ValueError(f"Invalid transform: {xform}")
    xforms.reverse()
    return reduce(operator.mul, xforms, Matrix.identity(4))


def load_shape(
    spec, materials: dict[str, Material], colors: dict[str, Color]
) -> tuple[Material, Matrix]:
    material_spec = spec["material"]
    if isinstance(material_spec, str):
        material = materials[material_spec]
    else:
        material = load_material(material_spec, colors)
    transform = load_transforms(spec.get("transforms", []))
    return material, transform


def load_shapes(
    shapeslist: list[dict], materials: dict[str, Material], colors: dict[str, Color]
) -> list[Shape]:
    shapes: list[Shape] = []
    for spec in shapeslist:
        match spec:
            case {"sphere": shapeSpec}:
                material, transform = load_shape(shapeSpec, materials, colors)
                sphere = Sphere(material=material)
                sphere.transform = transform
                shapes.append(sphere)
            case {"plane": shapeSpec}:
                material, transform = load_shape(shapeSpec, materials, colors)
                plane = Plane(material=material)
                plane.transform = transform
                shapes.append(plane)
            case _:
                raise ValueError(f"Unsupported shape: {spec}")
    return shapes


def load_light(spec: dict, colors: dict[str, Color]) -> PointLight:
    try:
        x, y, z = spec["position"]
        kwargs: dict[str, Union[Point, Color]] = {"position": Point(x, y, z)}

        if "intensity" in spec:
            if isinstance(spec["intensity"], str):
                kwargs["intensity"] = colors[spec["intensity"]]
            else:
                kwargs["intensity"] = load_color(spec["intensity"])

        return PointLight(**kwargs)  # type: ignore
    except (ValueError, KeyError) as e:
        raise ValueError(f"Invalid light spec: {spec}") from e


def load_lights(specs: list, colors: dict[str, Color]) -> list[PointLight]:
    return [load_light(spec, colors) for spec in specs]


def load_camera(spec: dict, world: World) -> Camera:
    camera = Camera(
        hsize=spec["hsize"],
        vsize=spec["vsize"],
        field_of_view=p(spec["field_of_view"]),
    )
    view_xform = spec["view_transform"]
    from_ = Point(*view_xform["from"])
    to = Point(*view_xform["to"])
    up = Vector3(*view_xform["up"])
    camera.transform = World.view_transform(from_=from_, to=to, up=up)
    return camera

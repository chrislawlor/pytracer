import argparse
import sys
from math import pi

from pytracer import (
    PPM,
    Camera,
    Color,
    Material,
    Matrix,
    Pattern,
    Plane,
    Point,
    PointLight,
    Sphere,
    Vector3,
    World,
    render,
)


def build_world() -> World:
    material = Material(
        color=Color(1, 1, 1), ambient=0.3, diffuse=0.9, specular=0.4, shininess=30
    )
    pattern = Pattern.stripes(Color.from_hex("547980"), Color.from_hex("9DE0AD"))
    pattern.transform = Matrix.scaling(0.2, 0.2, 0.2) * Matrix.rotation_y(pi / 2)
    material.pattern = pattern
    sphere = Sphere(material=material)
    sphere.transform = (
        Matrix.scaling(2, 2, 2)
        * Matrix.translation(0, 1.4, 0)
        * Matrix.rotation_z(pi / 2)
        * Matrix.rotation_x(pi / 2)
    )

    floor = Plane()
    floor_mat = Material(
        color=Color(1, 1, 1), ambient=0.3, diffuse=0.9, specular=0.9, shininess=150
    )
    pattern = Pattern.stripes(Color.from_hex("E8DDCB"), Color.from_hex("036564"))
    pattern.transform = Matrix.scaling(2, 2, 2) * Matrix.rotation_y(pi / 4)
    floor_mat.pattern = pattern
    floor.material = floor_mat
    light = PointLight(Point(-10, 5, -10))

    return World(shapes=[sphere, floor], lights=[light])


def build_camera(width=200, height=100):
    return Camera(
        hsize=width,
        vsize=height,
        field_of_view=pi / 3,
        transform=World.view_transform(
            from_=Point(0, 3, -10), to=Point(0, 2.5, 0), up=Vector3(0, 1, 0)
        ),
    )


def main(width=200, height=100):

    world = build_world()
    camera = build_camera(width, height)

    canvas = render(camera, world)

    PPM.save(canvas, sys.stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=200)
    parser.add_argument("--height", type=int, default=100)

    args = parser.parse_args()

    main(**args.__dict__)

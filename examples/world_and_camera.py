import argparse
import sys
from math import pi

from pytracer import (
    PPM,
    Camera,
    Color,
    Matrix,
    Point,
    PointLight,
    Sphere,
    Vector3,
    World,
    render,
)

WALL_COLOR = Color(1, 0.9, 0.9)


def build_shapes():
    floor = Sphere()
    floor.transform = Matrix.scaling(10, 0.01, 10)
    floor.material.color = WALL_COLOR
    floor.material.specular = 0
    floor.material.ambient = 0

    left_wall = Sphere()
    left_wall.transform = (
        Matrix.translation(0, 0, 5)
        * Matrix.rotation_y(-pi / 4)
        * Matrix.rotation_x(pi / 2)
        * Matrix.scaling(10, 0.01, 10)
    )
    left_wall.material = floor.material

    right_wall = Sphere()
    right_wall.transform = (
        Matrix.translation(0, 0, 5)
        * Matrix.rotation_y(pi / 4)
        * Matrix.rotation_x(pi / 2)
        * Matrix.scaling(10, 0.01, 10)
    )
    right_wall.material = floor.material

    middle = Sphere()
    middle.transform = Matrix.translation(-0.5, 1, 0.5)
    middle.material.color = Color(0.1, 1, 0.5)
    middle.material.diffuse = 0.7
    middle.material.specular = 0.3

    right = Sphere()
    right.transform = Matrix.translation(1.5, 0.5, -0.5) * Matrix.scaling(0.5, 0.5, 0.5)
    right.material.color = Color(0.5, 1, 0.1)
    right.material.diffuse = 0.7
    right.material.specular = 0.3

    left = Sphere()
    left.transform = Matrix.translation(-1.5, 0.33, -0.75) * Matrix.scaling(
        0.33, 0.33, 0.33
    )
    left.material.color = Color(1, 0.8, 0.1)
    left.material.diffuse = 0.7
    left.material.specular = 0.3

    return [floor, left_wall, right_wall, middle, right, left]


def build_world():
    return World(
        shapes=build_shapes(),
        lights=[
            PointLight(Point(-10, 10, -10)),
            PointLight(Point(8, 15, -10), intensity=Color(0.3, 0.3, 0.3)),
        ],
    )


def build_camera(width, height):
    c = Camera(width, height, pi / 3)
    c.transform = World.view_transform(
        Point(0, 1.5, -5), Point(0, 1, 0), Vector3(0, 1, 0)
    )
    return c


def main(width=100, height=50):
    world = build_world()
    camera = build_camera(width, height)
    canvas = render(camera, world)

    PPM.save(canvas, sys.stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=100)
    parser.add_argument("--height", type=int, default=50)
    args = parser.parse_args()

    main(**args.__dict__)

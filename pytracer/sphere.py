from .materials import Material
from .matrix import Matrix
from .primitives import Point, Vector3


class Shape:
    def __init__(self):
        self.transform = Matrix.identity(4)
        self.material = Material.default()


class Sphere(Shape):
    def normal_at(self, point: Point) -> Vector3:
        object_point = self.transform.inverse() * point
        object_normal = object_point - Point(0, 0, 0)
        world_normal = self.transform.inverse().transpose() * object_normal
        # translations can mess up w, but it should always be zero.
        # our Vector3 are immutable, so we create a new one.
        world_normal = Vector3(x=world_normal.x, y=world_normal.y, z=world_normal.z)
        return world_normal.normalize()

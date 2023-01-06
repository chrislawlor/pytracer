from .matrix import Matrix


class Shape:
    def __init__(self):
        self.transform = Matrix.identity(4)


class Sphere(Shape):
    pass

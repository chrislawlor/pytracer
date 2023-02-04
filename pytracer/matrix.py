from __future__ import annotations

import math
from functools import cached_property

import numpy as np

from .primitives import FourTuple


class Matrix:
    def __init__(self, cells: list[list[float | int]]):
        self.cells = np.array(cells, dtype=np.float64)
        if cells:
            width = len(cells[0])
            if not all([len(row) == width for row in cells]):
                raise ValueError(f" Cells have uneven rows: {cells}")
            self.height, self.width = self.cells.shape
        else:
            self.width = 0
            self.height = 0

    @classmethod
    def from_np_array(cls, cells: np.ndarray) -> Matrix:
        m = Matrix([])
        m.cells = cells
        m.height, m.width = cells.shape
        return m

    @classmethod
    def with_shape(cls, width: int, height: int, fill: int | float = 0) -> Matrix:
        cells = [[fill] * width for _ in range(height)]
        return cls(cells)

    @classmethod
    def identity(cls, size) -> Matrix:
        """Build identity matrix of shape size x size"""
        result = Matrix.with_shape(size, size)
        for i in range(size):
            result[i, i] = 1
        return result

    @classmethod
    def translation(cls, x: int | float, y: int | float, z: int | float) -> Matrix:
        """Create a 4x4 translation Matrix"""
        result = cls.identity(4)
        result[0, 3] = x
        result[1, 3] = y
        result[2, 3] = z
        return result

    @classmethod
    def scaling(cls, x: int | float, y: int | float, z: int | float) -> Matrix:
        """Create a 4x4 scaling Matrix"""
        return Matrix([[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]])

    @classmethod
    def rotation_x(cls, radians: int | float) -> Matrix:
        """Create a 4x4 Matrix for rotation around the X axis"""
        m = Matrix.identity(4)
        m[1, 1] = math.cos(radians)
        m[1, 2] = -math.sin(radians)
        m[2, 1] = math.sin(radians)
        m[2, 2] = math.cos(radians)
        return m

    @classmethod
    def rotation_y(cls, radians: int | float) -> Matrix:
        """Create a 4x4 Matrix for rotation around the Y axis"""
        m = Matrix.identity(4)
        m[0, 0] = math.cos(radians)
        m[0, 2] = math.sin(radians)
        m[2, 0] = -math.sin(radians)
        m[2, 2] = math.cos(radians)
        return m

    @classmethod
    def rotation_z(cls, radians: int | float) -> Matrix:
        """Create a 4x4 Matrix for rotation around the Z axis"""
        m = Matrix.identity(4)
        m[0, 0] = math.cos(radians)
        m[0, 1] = -math.sin(radians)
        m[1, 0] = math.sin(radians)
        m[1, 1] = math.cos(radians)
        return m

    @classmethod
    def shearing(cls, Xy, Xz, Yx, Yz, Zx, Zy) -> Matrix:
        """Create a 4x4 shear (skew) matrix"""
        return Matrix(
            [
                # fmt: off
                [ 1, Xy, Xz, 0],
                [Yx,  1, Yz, 0],
                [Zx, Zy,  1, 0],
                [ 0,  0,  0, 1],
                # fmt: on
            ]
        )

    def transpose(self) -> Matrix:
        """
        Transpose, return a new Matrix.
        """
        return Matrix.from_np_array(np.transpose(self.cells))

    @cached_property
    def determinant(self) -> float:
        """Calculate the determinant"""
        return np.linalg.det(self.cells)

    def submatrix(self, row: int, col: int) -> Matrix:
        """
        Return a new submatrix of this matrix, with the given
        row and col removed
        """
        cells = np.delete(self.cells, col, 1)
        cells = np.delete(cells, row, 0)
        return Matrix.from_np_array(cells)

    def minor(self, row: int, col: int) -> float:
        """
        Calculate the determinant of the submatrix at row, col.
        """
        submatrix = self.submatrix(row, col)
        return submatrix.determinant

    def cofactor(self, row: int, col: int) -> float:
        # if row + col is an odd number, negate the minor
        result = self.minor(row, col)
        if (row + col) % 2 == 0:
            return result
        return -result

    def is_invertible(self) -> bool:
        return self.determinant != 0

    def inverse(self) -> Matrix:
        """Return the inverse of this matrix"""
        # if not self.is_invertible():
        #     raise ValueError(f"Matrix is not invertible: {self}")
        return Matrix.from_np_array(np.linalg.inv(self.cells))

    def __getitem__(self, key: tuple[int, int]) -> float | int:
        col, row = key
        return self.cells[col][row]

    def __setitem__(self, key: tuple[int, int], value):
        col, row = key
        self.cells[col][row] = value

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Matrix)
            and self.width == other.width
            and self.height == other.height
            and (self.cells == other.cells).all()
        )

    def __mul__(self, other: Matrix | FourTuple):
        if isinstance(other, Matrix):
            return self._mul_matrix(other)
        if isinstance(other, FourTuple):
            return self._mul_tuple(other)
        raise TypeError(f"Cannot multiply Matrix with type {type(other)}")

    def _mul_matrix(self, other: Matrix) -> Matrix:
        if self.width != other.height:
            raise ValueError(
                "Cannot multiply matrices where width of first is not equal "
                "to height of the second"
            )

        return Matrix.from_np_array(self.cells @ other.cells)

    def _mul_tuple(self, other: FourTuple) -> FourTuple:
        result = self._mul_matrix(Matrix([[other.x], [other.y], [other.z], [other.w]]))
        return FourTuple(*[c[0] for c in result.cells])

    def __repr__(self) -> str:
        return f"Matrix({self.cells})"

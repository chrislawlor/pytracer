from __future__ import annotations

import math
from functools import cached_property

from .primitives import FourTuple


class Matrix:
    def __init__(self, cells: list[list[float | int]]):
        self.cells = cells
        if cells:
            width = len(cells[0])
            if not all([len(row) == width for row in cells]):
                raise ValueError(f" Cells have uneven rows: {cells}")
            self.width = len(cells[0])
            self.height = len(cells)
        else:
            self.width = 0
            self.height = 0

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
        result = Matrix.identity(4)
        result[1, 1] = math.cos(radians)
        result[1, 2] = -math.sin(radians)
        result[2, 1] = math.sin(radians)
        result[2, 2] = math.cos(radians)
        return result

    def transpose(self) -> Matrix:
        """
        Transpose, return a new Matrix.
        """
        result = Matrix.with_shape(self.width, self.height)
        for row in range(self.height):
            for col in range(self.width):
                result[row, col] = self[col, row]
        return result

    @cached_property
    def determinant(self) -> float:
        """Calculate the determinant"""
        if self.width == 2 and self.height == 2:
            return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]

        return sum([self[0, col] * self.cofactor(0, col) for col in range(self.width)])

    def submatrix(self, row: int, col: int) -> Matrix:
        """
        Return a new submatrix of this matrix, with the given
        row and col removed
        """
        cells = []
        for row_i in range(self.height):
            if row_i != row:
                new_row = []
                for col_i in range(self.width):
                    if col_i != col:
                        new_row.append(self[row_i, col_i])
                cells.append(new_row)
        return Matrix(cells)

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
        if not self.is_invertible():
            raise ValueError(f"Matrix is not invertible: {self}")
        result = Matrix.with_shape(self.width, self.height)

        for row in range(self.height):
            for col in range(self.width):
                c = self.cofactor(row, col)

                # Note: "col, row" here, instead of "row, col",
                # accomplishes the transpose operation
                result[col, row] = c / self.determinant
        return result

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
            and self.cells == other.cells
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

        result = self.with_shape(other.width, other.height)
        for row in range(other.height):
            for col in range(other.width):
                result[row, col] = sum(
                    [self[row, i] * other[i, col] for i in range(self.width)]
                )
        return result

    def _mul_tuple(self, other: FourTuple) -> FourTuple:
        result = self * Matrix([[other.x], [other.y], [other.z], [other.w]])
        return FourTuple(*[c[0] for c in result.cells])

    def __repr__(self) -> str:
        return f"Matrix({self.cells})"
        return f"Matrix({self.cells})"

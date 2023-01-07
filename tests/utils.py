from functools import partial

import pytest

from pytracer.matrix import Matrix
from pytracer.primitives import FourTuple

EPSILON = 0.0001


approx = partial(pytest.approx, abs=EPSILON)


def assert_fourtuple_approx_equal(result: FourTuple, expected: FourTuple):
    assert result.x == approx(expected.x)
    assert result.y == approx(expected.y)
    assert result.z == approx(expected.z)
    assert result.w == approx(expected.w)


def assert_matrix_approx_equal(m1: Matrix, m2: Matrix):
    assert m1.width == m2.width
    assert m2.height == m2.height
    for row in range(m1.height):
        for col in range(m1.width):
            msg = (
                f"Matrices differ at [{row}, {col}]: "
                f"left: {m1[row, col]}, right: {m2[row, col]}"
            )
            assert m1[row, col] == approx(m2[row, col]), msg

import pytest

from pytracer.matrix import Matrix
from pytracer.primitives import FourTuple

from .utils import approx, assert_matrix_approx_equal


def test_getitem():
    m = Matrix(
        [[1, 2, 3, 4], [5.5, 6.5, 7.5, 8.5], [9, 10, 11, 12], [13.5, 14.5, 15.5, 16.5]]
    )
    assert m[0, 0] == 1
    assert m[0, 3] == 4
    assert m[1, 0] == 5.5
    assert m[1, 2] == 7.5
    assert m[2, 2] == 11
    assert m[3, 3] == 16.5
    with pytest.raises(IndexError):
        m[4, 4]


def test_equality():
    m1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    m2 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert m1 == m2


def test_inequality():
    m1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    m2 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
    assert m1 != m2


def test_assignment():
    m = Matrix.with_shape(3, 3)
    m[0, 0] = 1
    m[2, 2] = 4
    assert m == Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 4]])


def test_multiplying_4x4_matrices():
    m1 = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
    m2 = Matrix([[-2, 1, 2, 3], [3, 2, 1, -1], [4, 3, 6, 5], [1, 2, 7, 8]])
    assert m1 * m2 == Matrix(
        [[20, 22, 50, 48], [44, 54, 114, 108], [40, 58, 110, 102], [16, 26, 46, 42]]
    )


def test_multiplying_4x4_matrix_by_a_tuple():
    m = Matrix([[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]])
    t = FourTuple(1, 2, 3, 1)

    assert m * t == FourTuple(18, 24, 33, 1)


def test_build_identity_matrix():
    m = Matrix.identity(4)
    assert m == Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def test_multiply_by_identity_matrix():
    identity = Matrix.identity(4)
    m = Matrix([list(range(4)) for _ in range(4)])
    assert m * identity == m


def test_transpose_identity_matrix_is_identity_matrix():
    identity = Matrix.identity(4)
    assert identity.transpose() == identity


def test_transpose_matrix():
    m = Matrix([[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]])
    assert m.transpose() == Matrix(
        [[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]]
    )


def test_calculate_determinant_of_2x2_matrix():
    m = Matrix([[1, 5], [-3, 2]])
    assert m.determinant == 17


def test_submatrix_of_3x3_matrix_is_a_2x2_matrix():
    m = Matrix([[1, 5, 0], [-3, 2, 7], [0, 6, -3]])
    result = m.submatrix(0, 2)
    assert result == Matrix([[-3, 2], [0, 6]])


def test_submatrix_of_4x4_matrix_is_a_3x3_matrix():
    m = Matrix([[-6, 1, 1, 6], [-8, 5, 8, 6], [-1, 0, 8, 2], [-7, 1, -1, 1]])
    result = m.submatrix(2, 1)
    assert result == Matrix([[-6, 1, 6], [-8, 8, 6], [-7, -1, 1]])


def test_calculate_minor_of_3x3_matrix():
    m = Matrix([[3, 5, 0], [2, -1, -7], [6, -1, 5]])
    submatrix = m.submatrix(1, 0)
    assert submatrix.determinant == approx(25)
    assert m.minor(1, 0) == approx(25)


def test_calculate_cofactor_of_3x3_matrix():
    m = Matrix([[3, 5, 0], [2, -1, -7], [6, -1, 5]])
    assert m.minor(0, 0) == -12
    assert m.cofactor(0, 0) == -12
    assert m.minor(1, 0) == approx(25)
    assert m.cofactor(1, 0) == approx(-25)


def test_calculate_determinant_of_3x3_matrix():
    m = Matrix([[1, 2, 6], [-5, 8, -4], [2, 6, 4]])
    assert m.cofactor(0, 0) == approx(56)
    assert m.cofactor(0, 1) == approx(12)
    assert m.cofactor(0, 2) == -46
    assert m.determinant == approx(-196)


def test_calculate_determinant_of_4x4_matrix():
    m = Matrix([[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]])
    assert m.cofactor(0, 0) == approx(690)
    assert m.cofactor(0, 1) == approx(447)
    assert m.cofactor(0, 2) == approx(210)
    assert m.cofactor(0, 3) == approx(51)
    assert m.determinant == approx(-4071)


def test_an_invertible_matrix_for_invertibility():
    m = Matrix([[6, 4, 4, 4], [5, 5, 7, 6], [4, -9, 3, -7], [9, 1, 7, -6]])
    assert m.determinant == -2120
    assert m.is_invertible()


def test_non_invertible_matrix_for_invertibility():
    m = Matrix([[-4, 2, -2, 3], [9, 6, 2, 6], [0, -5, 1, -5], [0, 0, 0, 0]])
    assert m.determinant == 0
    assert not m.is_invertible()


def test_calculate_the_inverse_of_a_matrix():
    A = Matrix(
        [
            # fmt: off
            [-5,  2,  6, -8],
            [ 1, -5,  1,  8],
            [ 7,  7, -6, -7],
            [ 1, -3,  7,  4]
            # fmt: on
        ]
    )

    assert A.determinant == approx(532)
    assert A.cofactor(2, 3) == approx(-160)
    assert A.cofactor(3, 2) == approx(105)

    B = A.inverse()
    assert B[3, 2] == approx(-160 / 532)
    assert B[2, 3] == approx(105 / 532)

    assert_matrix_approx_equal(
        B,
        Matrix(
            [
                # fmt: off
                [ 0.21805,  0.45113,  0.24060, -0.04511],
                [-0.80827, -1.45677, -0.44361,  0.52068],
                [-0.07895, -0.22368, -0.05263,  0.19737],
                [-0.52256, -0.81391, -0.30075,  0.30639]
                # fmt: on
            ]
        ),
    )


def test_calculate_inverse_of_another_matrix():
    m = Matrix(
        [
            # fmt: off
            [ 8, -5,  9,  2],
            [ 7,  5,  6,  1],
            [-6,  0,  9,  6],
            [-3,  0, -9, -4],
            # fmt: on
        ]
    )
    expected = Matrix(
        [
            # fmt: off
            [-0.15385, -0.15385, -0.28205, -0.53846],
            [-0.07692,  0.12308,  0.02564,  0.03077],
            [ 0.35897,  0.35897,  0.43590,  0.92308],
            [-0.69231, -0.69231, -0.76923, -1.92308],
            # fmt: on
        ]
    )
    assert_matrix_approx_equal(m.inverse(), expected)


def test_multiply_a_product_by_its_inverse():
    m1 = Matrix([[3, -9, 7, 3], [3, -8, 2, -9], [-4, 4, 4, 1], [-6, 5, -1, 1]])
    m2 = Matrix([[8, 2, 2, 2], [3, -1, 7, 0], [7, 0, 5, 4], [6, -2, 0, 5]])
    m3 = m1 * m2
    assert_matrix_approx_equal(m3 * m2.inverse(), m1)

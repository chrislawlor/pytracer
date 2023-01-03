from math import isclose

EPSILON = 0.0001


def approx_equal(first: float, second: float):
    return isclose(first, second, rel_tol=EPSILON)

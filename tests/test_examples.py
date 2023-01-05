"""
Examples of tests. This is meant to be a reference
for writing real tests that need interesting types of assertions.
"""
import pytest

EPSILON = 0.0001


def test_assert_almost_equal():
    assert 2.0 == pytest.approx(1.9999, abs=EPSILON)

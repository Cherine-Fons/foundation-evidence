import pytest

from finance_utils import future_value, mean_return, simple_return


def test_simple_return():
    assert simple_return(100, 110) == pytest.approx(0.1)


def test_future_value():
    assert future_value(1000, 0.10, 2) == pytest.approx(1210.0)


def test_mean_return():
    assert mean_return([0.1, 0.2, 0.3]) == pytest.approx(0.2)

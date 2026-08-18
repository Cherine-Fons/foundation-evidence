import pytest


def simple_return(old_price: float, new_price: float) -> float:
    return (new_price - old_price) / old_price


def test_simple_return():
    assert simple_return(100, 110) == pytest.approx(0.1)




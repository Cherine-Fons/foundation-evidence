import numpy as np


def simple_return(old_price: float, new_price: float) -> float:
    return (new_price - old_price) / old_price


def future_value(principal: float, annual_rate: float, years: int) -> float:
    return principal * (1 + annual_rate) ** years


def mean_return(returns):
    returns_array = np.array(returns)
    return returns_array.mean()

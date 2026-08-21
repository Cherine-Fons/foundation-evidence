import helpers


def test_is_admissible_even_and_ordered():
    assert helpers.is_admissible(2, 4) == True

def test_count_degrees_double_edge():
    assert helpers.count_degrees([(0, 1), (0, 1)]) == {0: 2, 1: 2}

def test_abs_diffs_basic():
    assert helpers.abs_diffs([10, 13, 8]) == [3, 5]

def test_find_over_capacity_strict():
    assert helpers.find_over_capacity({0: 3}, {0: 3}) == [] 

def test_is_admissible_equal():
    assert helpers.is_admissible(3, 3) == True
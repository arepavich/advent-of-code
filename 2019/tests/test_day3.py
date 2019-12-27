import pytest

import day3


@pytest.mark.parametrize(
    "test_input, expected", (
            ((1, 0), 1),
            ((1, 1), 2),
            ((1, -1), 2),
            ((-1, 1), 2)
    )
)
def test_can_get_correct_distance(test_input, expected):
    ret_val = day3.get_distance(*test_input)
    assert ret_val == expected


@pytest.mark.parametrize(
    "intersections, expected", (
            ([(38, 121), (180, 45)], 159),
            ([(110, 85), (80, 55)], 135)
    )
)
def test_can_get_correct_intersection(intersections, expected):
    assert day3.get_distance_closest(intersections) == expected

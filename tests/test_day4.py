import pytest

import day4


@pytest.mark.parametrize(
    "test_input, expected", (
            (111111, True),
            (223450, False),
            (123789, False),
    )
)
def test_can_get_correct_result_from_meets_criteria(test_input, expected):
    assert day4.password_meets_incomplete_criteria(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected", (
            (112233, True),
            (123444, False),
            (111122, True)
    )
)
def test_can_get_correct_result_from_password_meets_criteria(test_input, expected):
    assert day4.password_meets_criteria(test_input) == expected

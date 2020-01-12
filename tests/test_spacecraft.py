from unittest import mock

import pytest

import spacecraft


class TestModule(object):
    @pytest.mark.parametrize("test_input", [12, 14, 1969, 100756])
    def test_mass(self, test_input):
        assert spacecraft.Module(test_input).mass == test_input

    @pytest.mark.parametrize("test_input, expected", [(12, 2), (14, 2), (1969, 654), (100756, 33583)])
    def test_matter_fuel_requirement(self, test_input, expected):
        assert spacecraft.Module(test_input).matter_fuel_requirement == expected


class TestFuel(object):
    @pytest.mark.parametrize("test_input, expected", [(14, 2), (1969, 966), (100756, 50346)])
    def test_fuel_requirement(self, test_input, expected):
        assert spacecraft.Fuel(test_input).fuel_requirement == expected


class TestSpacecraft(object):
    @pytest.mark.parametrize("test_input, expected", [(14, 2), (1969, 966), (100756, 50346)])
    def test_fuel_requirement(self, test_input, expected):
        assert spacecraft.Spacecraft(modules=[spacecraft.Module(test_input)]).fuel_requirement == expected


class TestComputer(object):
    @pytest.fixture(scope="class")
    def fixture_computer(self):
        return spacecraft.Computer()

    @pytest.mark.parametrize("test_input, expected", [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ])
    def test_intcode_manipulates_input_correctly(self, test_input, expected, fixture_computer):
        assert fixture_computer.intcode(test_input) == expected

    @pytest.mark.parametrize(
        "test_input, prompt_input, expected", [
            ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
            ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 28, 1),
            ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
            ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 28, 1),
            ([
                 3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
             ], 6, 999),
            ([
                 3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
             ], 8, 1000),
            ([
                 3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
             ], 28, 1001),
        ]
    )
    def test_intcode_processes_correctly(self, test_input, prompt_input, expected, monkeypatch, fixture_computer):
        mock_input = mock.MagicMock(return_value=str(prompt_input))
        monkeypatch.setattr('builtins.input', mock_input)

        mock_print = mock.MagicMock()
        monkeypatch.setattr('builtins.print', mock_print)

        fixture_computer.intcode(test_input)
        mock_print.assert_called_once_with(expected)

    def test_intcode_can_add(self, fixture_computer):
        assert fixture_computer.intcode([1, 2, 2, 3, 99]) == [1, 2, 2, 4, 99]

    def test_intcode_can_multiply(self, fixture_computer):
        assert fixture_computer.intcode([2, 1, 2, 3, 99]) == [2, 1, 2, 2, 99]

    def test_intcode_can_store_value(self, monkeypatch, fixture_computer):
        input_value = 8
        mock_input = mock.MagicMock(return_value=str(input_value))
        monkeypatch.setattr('builtins.input', mock_input)
        assert fixture_computer.intcode([3, 0, 99]) == [input_value, 0, 99]

    def test_intcode_can_print_value(self, monkeypatch, fixture_computer):
        mock_print = mock.MagicMock()
        monkeypatch.setattr('builtins.print', mock_print)

        fixture_computer.intcode([4, 0, 99])
        mock_print.assert_called_once_with(4)

    def test_intcode_raises_exception_with_invalid_instruction(self, fixture_computer):
        with pytest.raises(ValueError):
            fixture_computer.intcode([0, 99])

    @pytest.mark.parametrize(
        "test_input, expected", [
            ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
        ]
    )
    def test_intcode_can_interpret_param_modes(self, test_input, expected, fixture_computer):
        assert fixture_computer.intcode(test_input) == expected

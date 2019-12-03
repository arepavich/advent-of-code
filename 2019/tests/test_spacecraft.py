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
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99])
    ])
    def test_intcode(self, test_input, expected, fixture_computer):
        assert fixture_computer.intcode(test_input) == expected

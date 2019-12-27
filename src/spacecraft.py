import math


class Spacecraft(object):
    """A spacecraft consisting of an arbitrary number of modules."""

    def __init__(self, modules=None):
        self._modules = modules or []
        self._mass = None

    def add_module(self, module):
        """Adds a module to the spacecraft.

        Args:
            module: A Module instance to be added to the spacecraft.
        """
        if isinstance(module, Module):
            self._modules.append(module)
            self._mass = None

    @property
    def mass(self):
        """Returns the total mass of the spacecraft."""

        if self._mass is None:
            self._calculate_mass()

        return self._mass

    def _calculate_mass(self):
        self._mass = 0
        for module in self._modules:
            self._mass += module.mass

    @property
    def fuel_requirement(self):
        """Returns an integer indicating the amount of fuel required to get the spaceship into orbit."""

        total_fuel = 0
        for module in self._modules:
            total_fuel += module.fuel_requirement

        return total_fuel


class Matter(object):
    """An abstract class to represent matter."""
    def __init__(self, mass=0):
        self._mass = mass

    @property
    def mass(self):
        """Returns an integer representing this matter's mass."""

        return self._mass

    @property
    def matter_fuel_requirement(self):
        """Calculates the amount of fuel required to launch this matter based on its mass.

        Returns:
            An integer representing the amount of fuel required to carry this matter's mass into orbit.
        """

        return int(math.floor(self.mass / 3) - 2)

    @property
    def fuel_requirement(self):
        """Calculates the total amount of fuel required to launch this module and its required fuel.

        Returns:
            An integer representing the total amount of fuel required to launch this matter's mass
            along with its additional required fuel.
        """

        return self.matter_fuel_requirement + Fuel(self.matter_fuel_requirement).fuel_requirement


class Fuel(Matter):
    """A class representing some quantity of fuel."""

    @property
    def fuel_requirement(self):
        """Returns an integer representing the amount of additional fuel necessary to launch this fuel's mass."""

        qty = self.matter_fuel_requirement

        if qty > 0:
            qty += Fuel(qty).fuel_requirement
            return qty
        else:
            return 0


class Module(Matter):
    """An abstract class to represent a ship module."""

    pass


class Computer(Module):
    """A computer ship module."""

    ADD = 1
    MULT = 2
    HALT = 99
    VALID_INSTRUCTIONS = {
        ADD: {
            'parameters': 3
        },
        MULT: {
            'parameters': 3
        },
        HALT: {
            'parameters': 0
        }
    }

    def intcode(self, input_list):
        """Processes a series of intcode instructions.

        Args:
            input_list: A list of integers representing the intcode instructions to be processed.

        Returns:
            A list resulting from processing each of the instructions in the provided intcode list.

        Raises:
            ValueError: An invalid instruction was detected.
        """

        index = 0
        while index < len(input_list):
            instruction = input_list[index]

            if instruction not in self.VALID_INSTRUCTIONS.keys():
                raise ValueError(f"Invalid instruction at {index}")

            inst_meta = self.VALID_INSTRUCTIONS.get(instruction)

            if instruction == self.HALT:
                break
            else:
                first = input_list[input_list[index + 1]]
                second = input_list[input_list[index + 2]]
                output = input_list[index + 3]

                if instruction == self.ADD:
                    input_list[output] = first + second
                elif instruction == self.MULT:
                    input_list[output] = first * second

            index += inst_meta.get('parameters', 0) + 1

        return input_list

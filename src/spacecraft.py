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

            # Force recalculation of mass next time it is accessed
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
    STORE = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99
    VALID_INSTRUCTIONS = {
        ADD: {
            'parameters': 3,
            'output_param': 3
        },
        MULT: {
            'parameters': 3,
            'output_param': 3
        },
        HALT: {
            'parameters': 0
        },
        STORE: {
            'parameters': 1,
            'output_param': 1
        },
        OUTPUT: {
            'parameters': 1
        },
        JUMP_IF_TRUE: {
            'parameters': 2
        },
        JUMP_IF_FALSE: {
            'parameters': 2
        },
        LESS_THAN: {
            'parameters': 3,
            'output_param': 3
        },
        EQUALS: {
            'parameters': 3,
            'output_param': 3
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

        def parse_instruction(my_inst):
            """Returns a tuple indicating the op code and list of parameter modes for a given instruction."""

            instruction_ = str(my_inst)
            if len(instruction_) > 1:
                op_code = int(''.join(instruction_[-2:]))
                modes_ = [int(mode_) for mode_ in reversed(instruction_[:-2])]
            else:
                op_code = my_inst
                modes_ = []
            return op_code, modes_

        index = 0
        while index < len(input_list):
            instruction, modes = parse_instruction(input_list[index])

            if instruction not in self.VALID_INSTRUCTIONS.keys():
                raise ValueError(f"Invalid instruction at {index}")

            inst_meta = self.VALID_INSTRUCTIONS.get(instruction)

            parameter_count = inst_meta.get('parameters', 0)
            output_param = inst_meta.get('output_param')
            parameters = []
            param_start_index = index + 1
            for i, param in enumerate(input_list[param_start_index:param_start_index+parameter_count]):
                # Default to mode 0 (position mode)
                mode = modes[i] if i < len(modes) else 0

                parameters.append(
                    param if mode == 1 or (output_param is not None and i == (output_param - 1)) else input_list[param]
                )

            if instruction == self.HALT:
                break
            elif instruction in (self.ADD, self.MULT, self.LESS_THAN, self.EQUALS):
                # Add, multiply, less than, and equals functions use the same parameter format
                first, second, output = parameters

                if instruction == self.ADD:
                    input_list[output] = first + second
                elif instruction == self.MULT:
                    input_list[output] = first * second
                elif instruction == self.LESS_THAN:
                    input_list[output] = 1 if first < second else 0
                elif instruction == self.EQUALS:
                    input_list[output] = 1 if first == second else 0
            elif instruction == self.STORE:
                target = parameters[0]
                value = int(input("Enter a value to store: "))

                input_list[target] = value
            elif instruction == self.OUTPUT:
                value = parameters[0]
                print(value)
            elif instruction == self.JUMP_IF_TRUE:
                value, target = parameters
                if value != 0:
                    index = target
                    continue
            elif instruction == self.JUMP_IF_FALSE:
                value, target = parameters
                if value == 0:
                    index = target
                    continue

            index += parameter_count + 1

        return input_list

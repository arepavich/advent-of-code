import math


class Spacecraft(object):
    def __init__(self, modules=None):
        self._modules = modules or []
        self._mass = None

    def add_module(self, module):
        if isinstance(module, Module):
            self._modules.append(module)
            self._mass = None

    @property
    def mass(self):
        if self._mass is None:
            self._calculate_mass()

        return self._mass

    def _calculate_mass(self):
        self._mass = 0
        for module in self._modules:
            self._mass += module.mass

    @property
    def fuel_requirement(self):
        total_fuel = 0
        for module in self._modules:
            total_fuel += module.fuel_requirement

        return total_fuel


class Matter(object):
    def __init__(self, mass):
        self._mass = mass

    @property
    def mass(self):
        return self._mass

    @property
    def matter_fuel_requirement(self):
        return int(math.floor(self.mass / 3) - 2)

    @property
    def fuel_requirement(self):
        """Calculates the amount of fuel required to launch this module based on its mass"""
        return self.matter_fuel_requirement + Fuel(self.matter_fuel_requirement).fuel_requirement


class Fuel(Matter):
    @property
    def fuel_requirement(self):
        qty = self.matter_fuel_requirement

        if qty > 0:
            qty += Fuel(qty).fuel_requirement
            return qty
        else:
            return 0


class Module(Matter):
    pass


class Computer(Module):
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

    def __init__(self, mass=0):
        super(Computer, self).__init__(mass)

    def intcode(self, input_list):

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



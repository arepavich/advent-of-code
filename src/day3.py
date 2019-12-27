import os

import systems


def get_inputs():
    """Returns a list of strings read in from the input file."""

    with open(os.path.abspath(os.path.join("..", "inputs", "wire_paths.txt")), "rt") as in_file:
        inputs = in_file.readlines()

    return inputs


def construct_circuit(wire_instructions):
    """Creates and returns a FuelManagement instance with the provided wire instructions.

    Args:
        wire_instructions: A list of strings indicating the directions from which to create
        the FuelManagement object's wires.

    Returns:
        A FuelManagement instance with wires according to the provided wire instructions.
    """

    fm = systems.FuelManagement()
    for wire in wire_instructions:
        fm.add_wire(wire)

    return fm


def part1():
    """Processes part 1 of the puzzle for day 3."""

    fm = construct_circuit(get_inputs())
    print(fm.get_distance_to_closest_intersection())


def part2():
    """Processes part 2 of the puzzle for day 3."""

    fm = construct_circuit(get_inputs())
    print(fm.get_lowest_latency_intersection())


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()

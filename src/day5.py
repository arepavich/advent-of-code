import os

import spacecraft


def get_inputs():
    """Returns a list of integers representing the instructions to be processed."""

    with open(os.path.abspath(os.path.join("..", "inputs", "day5_inputs.txt")), "rt") as in_file:
        inputs = in_file.read().strip().split(',')

    return [int(input_) for input_ in inputs]


def main():
    """Processes the challenge for day 5."""

    # When prompted, input for part 1 must be `1`, input for part 2 must be `5`
    inputs = get_inputs()
    computer = spacecraft.Computer()
    computer.intcode(inputs)


if __name__ == '__main__':
    main()

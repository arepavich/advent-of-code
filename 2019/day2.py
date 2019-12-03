import os

import spacecraft


def get_inputs():
    with open(os.path.join("inputs", "intcode_inputs.txt"), "rt") as in_file:
        inputs = in_file.read().strip().split(',')

    return [int(input_) for input_ in inputs]


def part2():
    orig_inputs = get_inputs()
    target_value = 19690720
    for noun in range(0, 100):
        for verb in range(0, 100):
            inputs = orig_inputs.copy()
            inputs[1] = noun
            inputs[2] = verb
            output = spacecraft.Computer().intcode(inputs)
            if output[0] == target_value:
                print(f"Noun: {noun}, Verb: {verb}")
                print(f"Answer (100 * noun + verb): {(100 * noun) + verb}")
                break


def part1():
    inputs = get_inputs()
    computer = spacecraft.Computer()
    inputs[1] = 12
    inputs[2] = 2
    print(computer.intcode(inputs)[0])


if __name__ == '__main__':
    part1()
    part2()

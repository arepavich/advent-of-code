import os

import spacecraft


def part2():
    with open(
            os.path.join("inputs", "ship_modules.txt"),
            "rt"
    ) as in_file:
        inputs = in_file.readlines()

    ship = spacecraft.Spacecraft()

    for input_ in inputs:
        ship.add_module(spacecraft.Module(int(input_.strip())))

    print(ship.fuel_requirement)


def part1():
    total_fuel = 0
    with open(
            os.path.join("inputs", "ship_modules.txt"),
            "rt"
    ) as in_file:
        inputs = in_file.readlines()

    for input_ in inputs:
        my_module = spacecraft.Module(int(input_.strip()))
        total_fuel += my_module.matter_fuel_requirement

    print(total_fuel)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()

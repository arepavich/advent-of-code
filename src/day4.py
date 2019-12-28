RANGE_MIN = 183564
RANGE_MAX = 657474


def password_meets_incomplete_criteria(password):
    """Checks a password against the incomplete criteria provided (for part 1).

    Args:
        password: An integer representing the password to check against the criteria.

    Returns:
        A boolean indicating whether the password meets the criteria.

    Raises:
        TypeError: The password provided is not of type `int`.
    """

    if not isinstance(password, int):
        raise TypeError(f"Value for password is of invalid type. Requires an integer, but received {type(password)}.")

    pw_string = str(password)
    has_matching_adjacent = False
    for a, b in zip(pw_string, pw_string[1:]):
        if int(b) < int(a):
            return False

        if a == b:
            has_matching_adjacent = True

    return has_matching_adjacent


def password_meets_criteria(password):
    """Checks a password against the full criteria provided (including part 2).

    Args:
        password: An integer representing the password to check against the criteria.

    Returns:
        A boolean indicating whether the password meets the criteria.

    Raises:
        TypeError: The password provided is not of type `int`.
    """

    if not isinstance(password, int):
        raise TypeError(f"Value for password is of invalid type. Requires an integer, but received {type(password)}.")

    pw_string = str(password)
    has_matching_adjacent = False
    matched = None
    prev_a = None
    for a, b in zip(pw_string, pw_string[1:]):
        if int(b) < int(a):
            return False

        if a == b and matched is None:
            has_matching_adjacent = True
            matched = a

        if prev_a is not None and prev_a == b and prev_a == matched:
            has_matching_adjacent = False
            matched = None

        prev_a = a

    return has_matching_adjacent


def part1():
    """Processes part 1 of the puzzle for day 4."""
    num_possibilities = 0
    for x in range(RANGE_MIN, RANGE_MAX):
        if password_meets_incomplete_criteria(x):
            num_possibilities += 1

    print(num_possibilities)


def part2():
    """Processes part 2 of the puzzle for day 4."""
    num_possibilities = 0
    for x in range(RANGE_MIN, RANGE_MAX):
        if password_meets_criteria(x):
            num_possibilities += 1

    print(num_possibilities)


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()

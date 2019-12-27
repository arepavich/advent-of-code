import os

import systems


def get_inputs():
    """Returns a list of strings read in from the input file."""

    with open(os.path.abspath(os.path.join("..", "inputs", "wire_paths.txt")), "rt") as in_file:
        inputs = in_file.readlines()

    return inputs


def get_distance(x, y):
    """Returns the Manhattan distance of a point relative to the point of origin.

    Args:
        x: The x coordinate of the point for which the distance should be calculated.
        y: The y coordinate of the point for which the distance should be calculated.

    Returns:
        An integer indicating the distance of the provided point from the point of origin.
    """

    return abs(x) + abs(y)


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


def get_distance_closest(intersections):
    """Returns the shortest direct Manhattan distance to an intersection.

    Identifies the intersection closest to the point of origin and returns
    the distance of that intersection from the origin.

    Args:
        intersections: A list of coordinates indicating the location of intersections.

    Returns:
        An integer indicating the shortest Manhattan distance to an intersection.
    """

    closest_intersection = {}

    for intersection in intersections:
        distance = get_distance(*intersection)
        best_distance = closest_intersection.get('distance')
        if best_distance is None or distance < best_distance:
            closest_intersection['coordinates'] = intersection
            closest_intersection['distance'] = distance

    return closest_intersection['distance']


def get_shortest_combined_distance(fm, intersections):
    """Returns the shortest combined number of steps to any intersection.

    Checks distance along each wire (following the path of the wire) to reach each intersection,
    and determines the shortest combined distance to reach an intersection.

    Args:
        fm: A FuelManagement instance which contains the wires along which the intersections reside.
        intersections: A list of coordinates indicating the location of intersections.

    Returns:
        An integer indicating the shortest combined distance along the wires to an intersection.
    """

    min_distance = None

    for intersection in intersections:
        combined_distance = 0
        for wire in fm.wires:
            combined_distance += wire.distance_to_point(intersection)

        if min_distance is None or combined_distance < min_distance:
            min_distance = combined_distance

    return min_distance


def main():
    wire_inputs = get_inputs()
    fm = construct_circuit(wire_inputs)

    intersections = fm.find_intersections()

    # Part 1
    print(get_distance_closest(intersections))

    # Part 2
    print(get_shortest_combined_distance(fm, intersections))


if __name__ == '__main__':
    main()

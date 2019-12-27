import spacecraft


class Coordinate(tuple):
    """A subclass of tuple with dedicated properties for x and y values for ease of access and readability."""

    def __new__(cls, x, y):
        return tuple.__new__(Coordinate, (x, y))

    @property
    def x(self):
        """Returns the x coordinate."""

        return self[0]

    @property
    def y(self):
        """Returns the y coordinate."""

        return self[1]


class FuelManagement(spacecraft.Module):
    """A FuelManagement ship module consisting of multiple wires."""

    def __init__(self):
        super(FuelManagement, self).__init__()
        self.wires = []
        self._intersections = None

    def add_wire(self, wire):
        """Adds a wire to the FuelManagement ship module.

        Given a wire instance or set of instructions indicating the path of a wire,
        adds a new wire to the FuelManagement module.

        Args:
            wire: A predefined instance of Wire, or a string or list containing instructions for creation
            of a new Wire instance to be added to the FuelManagement module.

        Raises:
            TypeError: An invalid value was provided for `wire`. Must be an instance of Wire or a str or list containing
            instructions for creating a new Wire instance.
        """

        if isinstance(wire, Wire):
            self.wires.append(wire)
        elif isinstance(wire, str) or isinstance(wire, list):
            self.wires.append(Wire(wire))
        else:
            raise TypeError(
                f"Invalid type for value `instructions`. Expected an instance of `Wire` or a `str` or `list` "
                f"indicating instructions for creating a `Wire` instance"
            )

    def _find_intersections(self):
        intersections = []

        already_processed = []
        for wire in self.wires:
            for segment1 in wire.segments:
                for other_wire in self.wires:
                    if other_wire is wire or other_wire in already_processed:
                        # Skip if the wire is being compared to itself or has already been processed
                        continue

                    for segment2 in other_wire.segments:
                        intersection = segment1.intersects_at(segment2)
                        if intersection is not None:
                            intersections.append(intersection)

            already_processed.append(wire)

        # Remove the point of origin from the list of intersections
        while (0, 0) in intersections:
            intersections.remove((0, 0))

        # Convert list of intersections to a set to eliminate duplicates
        return set(intersections)

    @property
    def intersections(self):
        """Returns a set of coordinates at which intersections of the FuelManagement module's wires occur."""

        if self._intersections is None:
            self._intersections = self._find_intersections()

        return self._intersections

    def get_distance_to_closest_intersection(self):
        """Returns the shortest direct Manhattan distance to an intersection.

        Identifies the intersection closest to the point of origin and returns
        the distance of that intersection from the origin.

        Returns:
            An integer indicating the shortest Manhattan distance to an intersection.
        """

        def get_distance(x, y):
            """Returns the Manhattan distance of a point relative to the point of origin.

            Args:
                x: The x coordinate of the point for which the distance should be calculated.
                y: The y coordinate of the point for which the distance should be calculated.

            Returns:
                An integer indicating the distance of the provided point from the point of origin.
            """

            return abs(x) + abs(y)

        closest_intersection = {}

        for intersection in self.intersections:
            distance = get_distance(*intersection)
            best_distance = closest_intersection.get('distance')
            if best_distance is None or distance < best_distance:
                closest_intersection['coordinates'] = intersection
                closest_intersection['distance'] = distance

        return closest_intersection['distance']

    def get_lowest_latency_intersection(self):
        """Returns the shortest combined number of steps to any intersection.

        Checks distance along each wire (following the path of the wire) to reach each intersection,
        and determines the shortest combined distance to reach an intersection.

        Returns:
            An integer indicating the shortest combined distance along the wires to an intersection.
        """

        min_distance = None

        for intersection in self.intersections:
            combined_distance = 0
            for wire in self.wires:
                combined_distance += wire.distance_to_point(intersection)

            if min_distance is None or combined_distance < min_distance:
                min_distance = combined_distance

        return min_distance


class Wire:
    """A Wire object consisting of WireSegment objects."""

    def __init__(self, instructions=None):
        """Initialize a new Wire instance, creating WireSegments from any instructions provided.

        Args:
            instructions: An optional string or list containing a series of instructions indicating the wire's path.

        Raises:
            TypeError: An invalid object type was provided for the `instructions` argument.
        """

        self._end_position = (0, 0)  # Wire always starts from same origin
        self.segments = []

        if instructions is not None:
            if isinstance(instructions, str):
                for instruction in instructions.split(','):
                    self.add_segment(instruction.strip())
            elif isinstance(instructions, list):
                for instruction in instructions:
                    self.add_segment(instruction)
            else:
                raise TypeError(
                    f"Invalid type for value `instructions`. Expected `str` or `list`, got `{type(instructions)}`"
                )

    @property
    def end_position(self):
        """Returns the coordinates corresponding to the very end of the wire."""

        if len(self.segments) > 0:
            self._end_position = self.segments[-1].end

        return self._end_position

    @property
    def points(self):
        """Returns a list of coordinates indicating the points at which each segment of the wire begins and ends.

        Raises:
            RuntimeError: A disconnect between consecutive WireSegments is detected.
        """

        points = [(0, 0)]
        if len(self.segments) > 0:
            for segment in self.segments:
                if segment.start != points[-1]:
                    raise RuntimeError(f"Wire is not continuous! Jumps from {points[-1]} to {segment.start}")

                points.append(segment.end)

        return points

    def distance_to_point(self, point):
        """Returns an integer indicating the distance required to reach the specified point along the wire.

        Args:
            point: A coordinate pair indicating the point for which distance along the wire should be calculated.
        """

        if not isinstance(point, Coordinate):
            point = Coordinate(*point)

        total_length = 0
        for segment in self.segments:
            if segment.intersects_point(point):
                if segment.orientation == WireSegment.HORIZONTAL:
                    intersect_length = segment.length - abs(segment.end.x - point.x)
                else:
                    intersect_length = segment.length - abs(segment.end.y - point.y)

                return total_length + intersect_length

            total_length += segment.length

    def add_segment(self, instruction):
        """Adds a new wire segment determined by an instruction input.

        Args:
            instruction: A string indicating a single instruction (`U23`, `R42`, etc.) for the wire segment.
        """

        offset_x, offset_y = self.parse_instruction(instruction)
        end_x, end_y = self.end_position

        new_x = end_x + offset_x
        new_y = end_y + offset_y

        self.segments.append(WireSegment(self.end_position, (new_x, new_y)))

    @staticmethod
    def parse_instruction(instruction: str):
        """Returns a coordinate offset determined by an instruction input.

        Args:
            instruction: A string containing the instruction to be parsed.

        Raises:
            ValueError: Value for `instruction` is invalid.
        """

        up = 'U'
        down = 'D'
        left = 'L'
        right = 'R'
        direction = instruction[0].upper()
        if direction not in (up, down, left, right):
            raise ValueError(f"Invalid instruction `{instruction}`")

        distance = int(instruction[1:])

        if direction == up:
            return 0, distance
        elif direction == down:
            return 0, -distance
        elif direction == left:
            return -distance, 0
        elif direction == right:
            return distance, 0


class WireSegment:
    """A WireSegment object."""

    HORIZONTAL = 'H'
    VERTICAL = 'V'

    def __init__(self, point1: tuple, point2: tuple):
        """Initializes a new instance of WireSegment.

        Raises:
            ValueError: One of the points provided is invalid or both points are the same.
        """
        if not (isinstance(point1, tuple) and isinstance(point1[0], int) and isinstance(point1[1], int)):
            raise ValueError(
                f"WireSegment points must be provided as tuples containing pairs of integers. "
                f"Received {point1} for point1."
            )
        if not (isinstance(point2, tuple) and isinstance(point2[0], int) and isinstance(point2[1], int)):
            raise ValueError(
                f"WireSegment points must be provided as tuples containing pairs of integers. "
                f"Received {point2} for point2."
            )

        self.start = Coordinate(*point1)
        self.end = Coordinate(*point2)
        if self.start == self.end:
            raise ValueError("A wire segment requires two different points.")

        self._length = None

    @property
    def orientation(self):
        """Returns a character indicating the orientation of the WireSegment."""

        if self.start.x != self.end.x:
            return self.HORIZONTAL
        elif self.start.y != self.end.y:
            return self.VERTICAL

    @property
    def length(self):
        """Returns an integer indicating the length of the WireSegment."""
        if self._length is None:
            self._length = (
                abs(self.start.x - self.end.x)
                if self.orientation == self.HORIZONTAL
                else abs(self.start.y - self.end.y)
            )

        return self._length

    def intersects_at(self, other_segment):
        """Calculates the point at which this WireSegment intersects another WireSegment.

        Calculates and returns the point at which this WireSegment intersects another given WireSegment.
        If the WireSegments do not intersect, None will be returned instead.

        Args:
            other_segment: The WireSegment for which an intersection point with this WireSegment should be calculated.

        Returns:
            A coordinate pair indicating the point at which this WireSegment intersects the
            WireSegment provided by `other_segment`. If no such intersection occurs, returns None.

        Raises:
            TypeError: An invalid value was provided for `other_segment`. This value must be an instance of WireSegment.
        """
        if not isinstance(other_segment, WireSegment):
            raise TypeError(
                f"intersects_at may only accept another instance of WireSegment. Received {type(other_segment)}"
            )

        if self.orientation == other_segment.orientation:
            return None

        if self.orientation == self.HORIZONTAL:
            if self._check_intersect(self, other_segment):
                return other_segment.start.x, self.start.y
        else:
            if self._check_intersect(other_segment, self):
                return self.start.x, other_segment.start.y

    def intersects_point(self, point):
        """Returns a boolean indicating whether this WireSegment passes through a given point.

        Args:
            point: A coordinate (or tuple which can be converted to a coordinate) representing the point
            for which an intersection should be detected.

        Returns:
            A boolean indicating whether this WireSegment passes through the provided point.
        """
        if not isinstance(point, Coordinate):
            point = Coordinate(*point)

        if self.orientation == self.HORIZONTAL:
            if self.start.y != point.y:
                return False

            return (self.start.x <= point.x <= self.end.x) or (self.end.x <= point.x <= self.start.x)
        elif self.orientation == self.VERTICAL:
            if self.start.x != point.x:
                return False

            return (self.start.y <= point.y <= self.end.y) or (self.end.y <= point.y <= self.start.y)

    @staticmethod
    def _check_intersect(h_seg, v_seg):
        does_intersect = ((h_seg.start.x <= v_seg.start.x <= h_seg.end.x)
                          or (h_seg.end.x <= v_seg.start.x <= h_seg.start.x))

        does_intersect = does_intersect and ((v_seg.start.y <= h_seg.start.y <= v_seg.end.y)
                                             or (v_seg.end.y <= h_seg.start.y <= v_seg.start.y))

        return does_intersect

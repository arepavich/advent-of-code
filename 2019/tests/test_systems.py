import pytest

import systems


class TestWire:
    @pytest.mark.parametrize(
        "test_input, expected", (
                (None, [(0, 0)]),
                ("U42", [(0, 0), (0, 42)]),
                ("D29,R39", [(0, 0), (0, -29), (39, -29)]),
                (["D29", "R39"], [(0, 0), (0, -29), (39, -29)])
        )
    )
    def test_init(self, test_input, expected):
        wire = systems.Wire(test_input)
        assert wire.points == expected

    def test_init_raises_exception_with_bad_instructions(self):
        with pytest.raises(TypeError):
            wire = systems.Wire({})

    @pytest.mark.parametrize(
        "test_input, expected", (
                ("U42", ((0, 0), (0, 42))),
                ("D29", ((0, 0), (0, -29))),
                ("L400", ((0, 0), (-400, 0))),
                ("R280", ((0, 0), (280, 0)))
        )
    )
    def test_can_add_segment(self, test_input, expected):
        wire = systems.Wire()
        wire.add_segment(test_input)
        segment = wire.segments[-1]
        assert (segment.start, segment.end) == expected

    @pytest.mark.parametrize(
        "test_input", (
                "U42,R22,D30",
                "D29,L44,U10",
                "L400,U369,L80",
                "R280,D33,L200"
        )
    )
    def test_points_raises_exception_when_segments_not_continuous(self, test_input):
        wire = systems.Wire(test_input)
        del wire.segments[1]
        with pytest.raises(RuntimeError):
            points = wire.points

    @pytest.mark.parametrize(
        "test_input, expected", (
                ("U42", (0, 42)),
                ("D29", (0, -29)),
                ("L400", (-400, 0)),
                ("R280", (280, 0))
        )
    )
    def test_parse_instruction(self, test_input, expected):
        assert systems.Wire().parse_instruction(test_input) == expected

    def test_parse_instruction_raises_exception_with_bad_instruction(self):
        with pytest.raises(ValueError):
            systems.Wire().parse_instruction("F320")

    @pytest.mark.parametrize(
        "test_wire, test_point, expected", (
                ("U1, R2, U1, L2", (1, 1), 2),
                ("U1, R2, U1, L2", (1, 2), 5),
                ("U1, R2, U1, L2, U3", (0, 5), 9)
        )
    )
    def test_can_get_distance_to_point(self, test_wire, test_point, expected):
        wire = systems.Wire(test_wire)
        ret_val = wire.distance_to_point(test_point)

        assert ret_val == expected


class TestWireSegment:
    def test_init(self):
        segment = systems.WireSegment((0, 0), (0, 1))
        assert segment.start == (0, 0)
        assert segment.end == (0, 1)

    def test_init_raises_exception_with_bad_input(self):
        with pytest.raises(ValueError):
            segment = systems.WireSegment((0, "apple"), (0, 1))

        with pytest.raises(ValueError):
            segment = systems.WireSegment((0, 1), (0, "apple"))

    def test_init_raises_exception_with_both_coordinates_same(self):
        with pytest.raises(ValueError):
            segment = systems.WireSegment((1, 1), (1, 1))

    @pytest.mark.parametrize(
        "test_input, expected", (
                (((0, 0), (0, 1)), systems.WireSegment.VERTICAL),
                (((30, 100), (30, 12)), systems.WireSegment.VERTICAL),
                (((0, 0), (1, 0)), systems.WireSegment.HORIZONTAL),
                (((80, 3), (42, 3)), systems.WireSegment.HORIZONTAL)
        )
    )
    def test_can_get_correct_orientation(self, test_input, expected):
        segment = systems.WireSegment(*test_input)
        assert segment.orientation == expected

    @pytest.mark.parametrize(
        "test_segment1, test_segment2, expected", (
                (((0, 1), (2, 1)), ((1, 0), (1, 2)), (1, 1)),
                (((33, 40), (70, 40)), ((42, 20), (42, 86)), (42, 40))
        )
    )
    def test_can_get_correct_intersection(self, test_segment1, test_segment2, expected):
        segment1 = systems.WireSegment(*test_segment1)
        segment2 = systems.WireSegment(*test_segment2)
        ret_val = segment1.intersects_at(segment2)

        assert ret_val == expected

    @pytest.mark.parametrize(
        "test_segment", (
                ((0, 1), (2, 1)),
                ((33, 40), (70, 40))
        )
    )
    def test_intersects_at_raises_exception_with_bad_input(self, test_segment):
        segment = systems.WireSegment(*test_segment)
        with pytest.raises(TypeError):
            segment.intersects_at("bad input")

    @pytest.mark.parametrize(
        "test_segment, expected", (
                (((0, 1), (2, 1)), 2),
                (((40, 33), (40, 70)), 37),
                (((20, 13), (-8, 13)), 28),
                (((17, 5), (17, -87)), 92)
        )
    )
    def test_can_get_correct_length(self, test_segment, expected):
        segment = systems.WireSegment(*test_segment)
        assert segment.length == expected

    @pytest.mark.parametrize(
        "test_segment, test_point, expected", (
                (((1, 2), (3, 2)), (2, 2), True),
                (((1, 2), (3, 2)), (1, 1), False),
                (((30, 196), (30, 122)), (30, 142), True),
                (((30, 196), (30, 122)), (30, 121), False)
        )
    )
    def test_can_call_intersects_point(self, test_segment, test_point, expected):
        segment = systems.WireSegment(*test_segment)
        assert segment.intersects_point(test_point) == expected


class TestFuelManagement:

    @pytest.fixture()
    def fm(self):
        return systems.FuelManagement()

    @staticmethod
    def check_wire_points(wire, points: list):
        assert wire.points == points

    def test_can_add_wire(self, fm):
        wire = systems.Wire()
        fm.add_wire(wire)
        assert wire in fm.wires

    def test_can_add_wire_by_instructions(self, fm):
        fm.add_wire("U42")
        self.check_wire_points(
            fm.wires[0],
            [
                (0, 0),
                (0, 42)
            ]
        )

    def test_can_add_wire_by_multipart_instructions(self, fm):
        fm.add_wire("U42,L400")
        self.check_wire_points(
            fm.wires[0],
            [
                (0, 0),
                (0, 42),
                (-400, 42)
            ]
        )

    def test_can_add_wire_by_list_instructions(self, fm):
        fm.add_wire(["U42"])
        self.check_wire_points(
            fm.wires[0],
            [
                (0, 0),
                (0, 42)
            ]
        )

    def test_add_wire_raises_exception_with_bad_instructions(self, fm):
        with pytest.raises(TypeError):
            fm.add_wire({})

    def test_can_find_an_intersection(self, fm):
        fm.add_wire("U1,R2")
        fm.add_wire("R1,U2")

        assert fm.intersections == {(1, 1)}

    @pytest.mark.parametrize(
        "test_wire1, test_wire2, expected", (
                ("U1, R2, U1, L2", "R1, U3", {(1, 1), (1, 2)}),
                ("R22, D30, L100, D25", "L2, D42, L56, U13, R81", {(-2, -30), (-58, -30), (22, -29)})
        )
    )
    def test_can_find_multiple_intersections(self, fm, test_wire1, test_wire2, expected):
        fm.add_wire(test_wire1)
        fm.add_wire(test_wire2)

        assert fm.intersections == expected

    @pytest.mark.parametrize(
        "test_wire1, test_wire2, expected", (
                ("U121, R180, D80", "R38, U280, R150, D235, L100", 159),
                ("U85, R120, L40, D35", "R110, U90, R25, D35, L60", 135)
        )
    )
    def test_can_get_distance_to_closest_intersection(self, fm, test_wire1, test_wire2, expected):
        fm.add_wire(test_wire1)
        fm.add_wire(test_wire2)

        assert fm.get_distance_to_closest_intersection() == expected

    @pytest.mark.parametrize(
        "test_wire1, test_wire2, expected", (
                ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 610),
                ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 410)
        )
    )
    def test_can_get_lowest_latency_intersection(self, fm, test_wire1, test_wire2, expected):
        fm.add_wire(test_wire1)
        fm.add_wire(test_wire2)

        assert fm.get_lowest_latency_intersection() == expected


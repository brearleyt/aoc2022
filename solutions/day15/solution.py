import dataclasses
import re
from pathlib import Path
from typing import Iterable, Optional

from ranges import Range, RangeSet  # type: ignore

from solutions.utils.input import lines_in_file


@dataclasses.dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def distance(self, other: "Coordinate") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclasses.dataclass(frozen=True)
class Sensor:
    location: Coordinate
    nearest_beacon: Coordinate
    radius: int

    @classmethod
    def from_def(cls, sensor_definition: str) -> "Sensor":
        match = re.match(
            r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+):"
            r" closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)",
            sensor_definition,
        )
        assert match

        sensor = Coordinate(x=int(match["sensor_x"]), y=int(match["sensor_y"]))
        beacon = Coordinate(x=int(match["beacon_x"]), y=int(match["beacon_y"]))
        radius = sensor.distance(beacon)
        return cls(location=sensor, nearest_beacon=beacon, radius=radius)

    def width_at_y(self, y: int) -> Optional[Range]:
        distance = abs(self.location.y - y)
        if distance > self.radius:
            return None
        diff = self.radius - distance
        start_x = self.location.x - diff
        end_x = self.location.x + diff
        return Range(start=start_x, end=end_x, include_end=True)

    def height(self) -> Range:
        return Range(
            start=self.location.y - self.radius,
            end=self.location.y + self.radius,
            include_end=True,
        )


def within_range_x_coordinates_at_y(sensors: Iterable[Sensor], y: int) -> RangeSet:
    possible_ranges = (s.width_at_y(y) for s in sensors)
    ranges = RangeSet(s for s in possible_ranges if s is not None)
    return ranges


def beacons_in_row(sensors: Iterable[Sensor], y: int) -> RangeSet:
    return RangeSet(
        Range(s.nearest_beacon.x, s.nearest_beacon.x, include_end=True)
        for s in sensors
        if s.nearest_beacon.y == y
    )


def out_of_range_coordinate_in_search_space(
    sensors: Iterable[Sensor], search_space_len: int
) -> Optional[Coordinate]:
    search_space = RangeSet(Range(0, search_space_len, include_end=True))
    x_range = search_space
    y_range = search_space - RangeSet(s.height() for s in sensors)

    for y in y_range:
        within_range = within_range_x_coordinates_at_y(sensors, y)
        out_of_range = x_range - within_range - beacons_in_row(sensors, y)
        if out_of_range:
            x = next(c.start + 1 for c in out_of_range)
            return Coordinate(x=x, y=y)

    return None


def part_1(sensors_def: list[str], y: int) -> int:
    sensors = [Sensor.from_def(d) for d in sensors_def]

    ranges = within_range_x_coordinates_at_y(sensors, y)
    ranges -= beacons_in_row(sensors, y)

    return sum(r.length() for r in ranges)


def part_2(sensors_def: list[str], search_space: int) -> int:
    sensors = [Sensor.from_def(d) for d in sensors_def]
    out_of_range = out_of_range_coordinate_in_search_space(sensors, search_space)
    assert out_of_range
    return out_of_range.x * 4000000 + out_of_range.y


if __name__ == "__main__":
    sensors_def = lines_in_file(Path("input.txt"))
    print(part_1(sensors_def, 2000000))
    print(part_2(sensors_def, 4000000))

import dataclasses
from pathlib import Path
from typing import Iterable, Optional

import networkx as nx  # type: ignore
from networkx import NetworkXNoPath

from solutions.utils.input import lines_in_file


@dataclasses.dataclass(frozen=True)
class Coordinate:
    row: int
    column: int

    def potential_neighbours(self) -> Iterable["Coordinate"]:
        yield Coordinate(row=self.row - 1, column=self.column)
        yield Coordinate(row=self.row + 1, column=self.column)
        yield Coordinate(row=self.row, column=self.column - 1)
        yield Coordinate(row=self.row, column=self.column + 1)


@dataclasses.dataclass(frozen=True)
class HeightMap:
    heights: dict[Coordinate, int]
    start: Coordinate
    end: Coordinate
    navigable_path: nx.DiGraph

    @classmethod
    def from_height_map_def(cls, height_map: list[str]) -> "HeightMap":
        heights = {
            coordinate: get_height(height_char)
            for coordinate, height_char in iter_coordinate_heights(height_map)
        }
        start = next(
            coordinate
            for coordinate, height_char in iter_coordinate_heights(height_map)
            if height_char == "S"
        )
        end = next(
            coordinate
            for coordinate, height_char in iter_coordinate_heights(height_map)
            if height_char == "E"
        )

        graph = nx.DiGraph()
        for coordinate, height in heights.items():
            for neighbour in coordinate.potential_neighbours():
                if neighbour not in heights:
                    continue
                neighbour_height = heights[neighbour]
                if neighbour_height - height <= 1:
                    graph.add_edge(coordinate, neighbour)

        return HeightMap(heights=heights, start=start, end=end, navigable_path=graph)

    def shortest_path_length(self, start: Optional[Coordinate] = None) -> Optional[int]:
        if start is None:
            start = self.start
        try:
            path = nx.shortest_path(self.navigable_path, start, self.end)
            return len(path) - 1
        except NetworkXNoPath:
            return None


def get_height(height_char: str) -> int:
    if height_char == "S":
        return ord("a")
    if height_char == "E":
        return ord("z")
    return ord(height_char)


def iter_coordinate_heights(height_map: list[str]) -> Iterable[tuple[Coordinate, str]]:
    for i, row in enumerate(height_map):
        for j, height_char in enumerate(row):
            yield Coordinate(row=i, column=j), height_char


def part_1(height_map: list[str]) -> int:
    map_ = HeightMap.from_height_map_def(height_map)
    shortest_path = map_.shortest_path_length()
    assert shortest_path
    return shortest_path


def part_2(height_map: list[str]) -> int:
    map_ = HeightMap.from_height_map_def(height_map)
    possible_starting_points = (
        c for c, height in map_.heights.items() if height == ord("a")
    )
    lengths = (map_.shortest_path_length(c) for c in possible_starting_points)
    return min(length for length in lengths if length)


if __name__ == "__main__":
    height_map = lines_in_file(Path("input.txt"))
    print(part_1(height_map))
    print(part_2(height_map))

import dataclasses
from functools import reduce
from pathlib import Path
from typing import Iterable

from solutions.utils.input import lines_in_file

Coordinate = tuple[int, int]


@dataclasses.dataclass(frozen=True)
class TreeMap:
    _width: int
    _height: int
    _tree_heights: list[int]

    @classmethod
    def from_trees(cls, trees: list[str]) -> "TreeMap":
        assert trees
        height = len(trees)
        width = len(trees[0])
        tree_heights = [int(tree) for row in trees for tree in row]
        return cls(_width=width, _height=height, _tree_heights=tree_heights)

    def iter_coordinates(self) -> Iterable[Coordinate]:
        for x in range(self._width):
            for y in range(self._height):
                yield x, y

    def is_visible(self, x: int, y: int) -> bool:
        assert self._is_valid_coordinate(x, y)

        height = self._tree_height(x, y)

        for way_out in self._ways_out(x, y):
            tree_heights = (self._tree_height(*coord) for coord in way_out)
            tallest = max(tree_heights, default=None)
            if tallest is None or tallest < height:
                return True

        return False

    def scenic_score(self, x: int, y: int) -> int:
        assert self._is_valid_coordinate(x, y)
        height = self._tree_height(x, y)
        scores = (
            self._way_out_score(height, way_out) for way_out in self._ways_out(x, y)
        )
        return reduce(lambda a, b: a * b, scores)

    def _tree_height(self, x: int, y: int) -> int:
        assert self._is_valid_coordinate(x, y)
        index = (self._width * y) + x
        return self._tree_heights[index]

    def _way_out_score(self, this_height: int, way_out: Iterable[Coordinate]) -> int:
        total = 0

        for coord in way_out:
            total += 1
            if self._tree_height(*coord) >= this_height:
                break

        return total

    def _ways_out(self, x: int, y: int) -> Iterable[Iterable[Coordinate]]:
        yield ((i, y) for i in reversed(range(x)))
        yield ((i, y) for i in range(x + 1, self._width))
        yield ((x, i) for i in reversed(range(y)))
        yield ((x, i) for i in range(y + 1, self._height))

    def _is_valid_coordinate(self, x: int, y: int) -> bool:
        return 0 <= x < self._width and 0 <= y < self._height


def part_1(trees: list[str]) -> int:
    tree_map = TreeMap.from_trees(trees)
    return sum(tree_map.is_visible(*coords) for coords in tree_map.iter_coordinates())


def part_2(trees: list[str]) -> int:
    tree_map = TreeMap.from_trees(trees)
    return max(tree_map.scenic_score(*coords) for coords in tree_map.iter_coordinates())


if __name__ == "__main__":
    _tree_heights = lines_in_file(Path("input.txt"))
    print(part_1(_tree_heights))
    print(part_2(_tree_heights))

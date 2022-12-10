import dataclasses
from enum import Enum
from pathlib import Path

from solutions.utils.input import lines_in_file


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"

    @property
    def is_x(self) -> bool:
        return self in {Direction.UP, Direction.DOWN}

    @property
    def step(self) -> int:
        if self in {Direction.UP, Direction.RIGHT}:
            return 1
        return -1

    def displacement(self, distance: int) -> int:
        return distance * self.step


@dataclasses.dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


@dataclasses.dataclass()
class Rope:
    head: Coordinate
    tail: Coordinate
    tail_positions: set[Coordinate]

    @classmethod
    def create(cls) -> "Rope":
        return cls(
            head=Coordinate(0, 0),
            tail=Coordinate(0, 0),
            tail_positions={Coordinate(0, 0)},
        )

    def move(self, direction: Direction, distance: int) -> None:
        displacement = direction.displacement(distance)
        if direction.is_x:
            new_positions = [
                Coordinate(x=self.head.x, y=y)
                for y in range(
                    self.tail.y + direction.step,
                    self.head.y + displacement,
                    direction.step,
                )
            ]
            self.head = Coordinate(x=self.head.x, y=self.head.y + displacement)
        else:
            new_positions = [
                Coordinate(x=x, y=self.head.y)
                for x in range(
                    self.tail.x + direction.step,
                    self.head.x + displacement,
                    direction.step,
                )
            ]
            self.head = Coordinate(x=self.head.x + displacement, y=self.head.y)

        if new_positions:
            self.tail = new_positions[-1]
        self.tail_positions |= set(new_positions)


def part_1(moves: list[str]) -> int:
    rope = Rope.create()
    for move in moves:
        direction, distance = move.split(" ")
        rope.move(Direction(direction), int(distance))
    return len(rope.tail_positions)


if __name__ == "__main__":
    moves = lines_in_file(Path("input.txt"))
    print(part_1(moves))

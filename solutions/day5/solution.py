import dataclasses
import re
from pathlib import Path
from queue import LifoQueue
from typing import Callable, Iterable, Optional, TypeVar

from solutions.utils.input import peek

_CRATE_WIDTH = 4

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class Move:
    number_of_crates: int
    from_stack_index: int
    to_stack_index: int

    @classmethod
    def from_move_line(cls, line: str) -> "Move":
        if match := re.match(
            r"move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)", line
        ):
            return cls(
                number_of_crates=int(match["count"]),
                from_stack_index=int(match["from"]) - 1,
                to_stack_index=int(match["to"]) - 1,
            )

        raise ValueError(f"Unexpected format for move line {line}")


StackMovingAlgorithm = Callable[[int, LifoQueue, LifoQueue], None]


def stack_mover_9000(
    number_of_crates: int, from_stack: LifoQueue[T], to_stack: LifoQueue[T]
) -> None:
    for _ in range(number_of_crates):
        to_stack.put(from_stack.get(block=False))


def stack_mover_9001(
    number_of_crates: int, from_stack: LifoQueue[T], to_stack: LifoQueue[T]
) -> None:
    tmp: LifoQueue[T] = LifoQueue(maxsize=number_of_crates)
    for _ in range(number_of_crates):
        tmp.put(from_stack.get(block=False))
    for _ in range(number_of_crates):
        to_stack.put(tmp.get(block=False))


def extract_crate_id(crate: str) -> Optional[str]:
    if match := re.match(r"\[(.)]", crate):
        return match.group(1)
    return None


def parse_row(line: str) -> dict[int, str]:
    crates = (line[i : i + _CRATE_WIDTH] for i in range(0, len(line), _CRATE_WIDTH))
    stacks = {
        stack_id: extract_crate_id(crate) for stack_id, crate in enumerate(crates)
    }
    return {
        stack_id: crate_id
        for stack_id, crate_id in stacks.items()
        if crate_id is not None
    }


def parse_stacks(crates: Iterable[str]) -> list[LifoQueue[str]]:
    crate_rows = [parse_row(crate) for crate in crates]
    number_of_stacks = max(len(stacks) for stacks in crate_rows)

    stacks: list[LifoQueue[str]] = [LifoQueue() for _ in range(number_of_stacks)]
    for crate_row in reversed(crate_rows):
        for stack_index, crate_id in crate_row.items():
            stacks[stack_index].put(crate_id)

    return stacks


def parse_moves(moves: Iterable[str]) -> list[Move]:
    return [Move.from_move_line(move) for move in moves]


def move_stacks(crates: list[str], stack_mover: StackMovingAlgorithm) -> str:
    deliminator = crates.index("\n")
    stacks = parse_stacks(crates[: deliminator - 1])
    moves = parse_moves(crates[deliminator + 1 :])

    for move in moves:
        from_stack = stacks[move.from_stack_index]
        to_stack = stacks[move.to_stack_index]
        stack_mover(move.number_of_crates, from_stack, to_stack)

    return "".join(peek(stack) for stack in stacks)


def part_1(crates: list[str]) -> str:
    return move_stacks(crates, stack_mover_9000)


def part_2(crates: list[str]) -> str:
    return move_stacks(crates, stack_mover_9001)


if __name__ == "__main__":
    with open(Path("input.txt"), encoding="utf-8") as f:
        pair_assignments = list(x for x in f)
    print(part_1(pair_assignments))
    print(part_2(pair_assignments))

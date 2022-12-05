from pathlib import Path
from queue import Queue
from typing import Callable, Iterator, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def newline_delineated_groups(
    input_: str, constructor: Callable[[str], R]
) -> Iterator[list[R]]:
    for group in input_.split("\n\n"):
        yield [constructor(i) for i in group.split("\n")]


def groups_from_file(file: Path, constructor: Callable[[str], R]) -> Iterator[list[R]]:
    with open(file, encoding="utf-8") as f:
        return newline_delineated_groups(f.read(), constructor)


def lines_in_file(file: Path) -> list[str]:
    with open(file, encoding="utf-8") as f:
        return list(x.strip() for x in f)


def chunked_iter(input_: list[T], chunk_size: int) -> Iterator[list[T]]:
    for i in range(0, len(input_), chunk_size):
        yield input_[i : i + chunk_size]


def peek(queue: Queue[T]) -> T:
    front = queue.get(block=False)
    queue.put(front)
    return front

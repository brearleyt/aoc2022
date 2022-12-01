from pathlib import Path
from typing import Callable, Iterator, TypeVar

R = TypeVar("R")


def newline_delineated_groups(
    input_: str, constructor: Callable[[str], R]
) -> Iterator[list[R]]:
    for group in input_.split("\n\n"):
        yield [constructor(i) for i in group.split("\n")]


def groups_from_file(file: Path, constructor: Callable[[str], R]) -> Iterator[list[R]]:
    with open(file, encoding="utf-8") as f:
        return newline_delineated_groups(f.read(), constructor)

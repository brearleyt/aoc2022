from pathlib import Path
from typing import Iterable

from solutions.utils.input import chunked_iter, lines_in_file


def points_for_char(char: str) -> int:
    if char.islower():
        return ord(char) - 96
    return ord(char) - 64 + 26


def types_in_each_compartment(rucksack: str) -> tuple[set[str], set[str]]:
    midpoint = len(rucksack) // 2
    compartment_a, compartment_b = rucksack[:midpoint], rucksack[midpoint:]
    return set(compartment_a), set(compartment_b)


def duplicated_type_in_rucksack(rucksack: str) -> str:
    compartment_a, compartment_b = types_in_each_compartment(rucksack)
    duplicated_types = compartment_a.intersection(compartment_b)
    assert len(duplicated_types) == 1
    return next(iter(duplicated_types))


def duplicated_type_in_rucksack_groups(groups: Iterable[str]) -> str:
    duplicated_types = set.intersection(*[set(rucksack) for rucksack in groups])
    assert len(duplicated_types) == 1
    return next(iter(duplicated_types))


def part_1(rucksacks: list[str]) -> int:
    return sum(
        points_for_char(duplicated_type_in_rucksack(rucksack)) for rucksack in rucksacks
    )


def part_2(rucksacks: list[str]) -> int:
    return sum(
        points_for_char(duplicated_type_in_rucksack_groups(group))
        for group in chunked_iter(rucksacks, chunk_size=3)
    )


if __name__ == "__main__":
    rucksacks = lines_in_file(Path("input.txt"))
    print(part_1(rucksacks))
    print(part_2(rucksacks))

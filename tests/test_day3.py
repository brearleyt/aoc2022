import pytest

from solutions.day3.solution import part_1, part_2


@pytest.fixture
def rucksacks() -> list[str]:
    return [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]


def test_part_1_returns_correct_value(rucksacks: list[str]) -> None:
    assert part_1(rucksacks) == 157


def test_part_2_returns_correct_value(rucksacks: list[str]) -> None:
    assert part_2(rucksacks) == 70

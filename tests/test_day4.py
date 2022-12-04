import pytest

from solutions.day4.solution import part_1, part_2


@pytest.fixture
def pair_assignments() -> list[str]:
    return ["2-4,6-8", "2-3,4-5", "5-7,7-9", "2-8,3-7", "6-6,4-6", "2-6,4-8"]


def test_part_1_returns_correct_value(pair_assignments: list[str]) -> None:
    assert part_1(pair_assignments) == 2


def test_part_2_returns_correct_value(pair_assignments: list[str]) -> None:
    assert part_2(pair_assignments) == 4

import pytest

from solutions.day8.solution import part_1, part_2


@pytest.fixture
def trees() -> list[str]:
    return ["30373", "25512", "65332", "33549", "35390"]


def test_part_1_returns_correct_value(trees: list[str]) -> None:
    assert part_1(trees) == 21


def test_part_2_returns_correct_value(trees: list[str]) -> None:
    assert part_2(trees) == 8

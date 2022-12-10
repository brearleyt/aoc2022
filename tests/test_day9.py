import pytest

from solutions.day9.solution import part_1


@pytest.fixture
def moves() -> list[str]:
    return ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]


def test_part_1_returns_correct_value(moves: list[str]) -> None:
    assert part_1(moves) == 13

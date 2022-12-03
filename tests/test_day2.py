import pytest

from solutions.day2.solution import part_1, part_2


@pytest.fixture
def games() -> list[str]:
    return ["A Y", "B X", "C Z"]


def test_part_1_returns_correct_value(games: list[str]) -> None:
    assert part_1(games) == 15


def test_part_2_returns_correct_value(games: list[str]) -> None:
    assert part_2(games) == 12

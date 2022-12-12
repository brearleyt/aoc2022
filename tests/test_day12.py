import pytest

from solutions.day12.solution import part_1, part_2


@pytest.fixture
def height_map() -> list[str]:
    return ["Sabqponm", "abcryxxl", "accszExk", "acctuvwj", "abdefghi"]


def test_part_1_returns_correct_value(height_map: list[str]) -> None:
    assert part_1(height_map) == 31


def test_part_2_returns_correct_value(height_map: list[str]) -> None:
    assert part_2(height_map) == 29

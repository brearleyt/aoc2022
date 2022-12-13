import pytest

from solutions.day13.solution import part_1, part_2


@pytest.fixture
def pairs() -> list[str]:
    return [
        "[1, 1, 3, 1, 1]",
        "[1, 1, 5, 1, 1]",
        "",
        "[[1], [2, 3, 4]]",
        "[[1], 4]",
        "",
        "[9]",
        "[[8, 7, 6]]",
        "",
        "[[4, 4], 4, 4]",
        "[[4, 4], 4, 4, 4]",
        "",
        "[7, 7, 7, 7]",
        "[7, 7, 7]",
        "",
        "[]",
        "[3]",
        "",
        "[[[]]]",
        "[[]]",
        "",
        "[1, [2, [3, [4, [5, 6, 7]]]], 8, 9]",
        "[1, [2, [3, [4, [5, 6, 0]]]], 8, 9]",
    ]


def test_part_1_returns_correct_value(pairs: list[str]) -> None:
    assert part_1(pairs) == 13


def test_part_2_returns_correct_value(pairs: list[str]) -> None:
    assert part_2(pairs) == 140

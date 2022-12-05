import pytest

from solutions.day5.solution import part_1, part_2


@pytest.fixture
def crates() -> list[str]:
    return [
        "    [D]    \n",
        "[N] [C]    \n",
        "[Z] [M] [P]\n",
        " 1   2   3 \n",
        "\n",
        "move 1 from 2 to 1\n",
        "move 3 from 1 to 3\n",
        "move 2 from 2 to 1\n",
        "move 1 from 1 to 2\n",
    ]


def test_part_1_returns_correct_value(crates: list[str]) -> None:
    assert part_1(crates) == "CMZ"


def test_part_2_returns_correct_value(crates: list[str]) -> None:
    assert part_2(crates) == "MCD"

import pytest

from solutions.day7.solution import part_1, part_2


@pytest.fixture
def terminal_lines() -> list[str]:
    return [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k",
    ]


def test_part_1_returns_correct_value(terminal_lines: list[str]) -> None:
    assert part_1(terminal_lines) == 95437


def test_part_2_returns_correct_value(terminal_lines: list[str]) -> None:
    assert part_2(terminal_lines) == 24933642

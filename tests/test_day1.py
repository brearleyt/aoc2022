from pathlib import Path

from solutions.day1.solution import part_1, part_2


def test_part_1_returns_correct_value(resources_dir: Path) -> None:
    f = resources_dir / "day1.txt"
    assert part_1(f) == 24000


def test_part_2_returns_correct_value(resources_dir: Path) -> None:
    f = resources_dir / "day1.txt"
    assert part_2(f) == 45000

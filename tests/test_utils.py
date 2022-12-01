from pathlib import Path

from solutions.utils.groups import groups_from_file


def test_group_splitter_returns_correct_groups(resources_dir: Path) -> None:
    input_ = resources_dir / "day1.txt"
    groups = list(groups_from_file(input_, int))

    expected_values = [
        [1000, 2000, 3000],
        [4000],
        [5000, 6000],
        [7000, 8000, 9000],
        [10000],
    ]
    assert groups == expected_values

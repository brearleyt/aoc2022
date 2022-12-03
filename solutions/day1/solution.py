import heapq
from pathlib import Path

from solutions.utils.input import groups_from_file


def _get_largest_n_calorie_sums(calories_list: Path, n: int) -> list[int]:
    calorie_groups = groups_from_file(calories_list, int)
    calorie_sums = (sum(x) for x in calorie_groups)
    return heapq.nlargest(n, calorie_sums)


def part_1(calories_list: Path) -> int:
    return max(_get_largest_n_calorie_sums(calories_list, 1))


def part_2(calories_list: Path) -> int:
    return sum(_get_largest_n_calorie_sums(calories_list, 3))


if __name__ == "__main__":
    print(part_1(Path("input.txt")))
    print(part_2(Path("input.txt")))

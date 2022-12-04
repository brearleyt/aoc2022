from pathlib import Path

from solutions.utils.input import lines_in_file


def _get_elf_pair_ranges(pair_assignment: str) -> tuple[range, range]:
    def get_elf_range(range_: str) -> range:
        start, end = range_.split("-")
        return range(int(start), int(end) + 1)

    elf_a, elf_b = pair_assignment.split(",")
    return get_elf_range(elf_a), get_elf_range(elf_b)


def _range_contains(container_range: range, contained_range: range) -> bool:
    """Tests if contained_range is fully contained within container_range"""
    return (
        container_range.start <= contained_range.start
        and contained_range.stop <= container_range.stop
    )


def _ranges_overlap(range_a: range, range_b: range) -> bool:
    return range_a.start < range_b.stop and range_a.stop > range_b.start


def part_1(pair_assignments: list[str]) -> int:
    pair_ranges = [_get_elf_pair_ranges(assignment) for assignment in pair_assignments]
    return sum(_range_contains(a, b) or _range_contains(b, a) for a, b in pair_ranges)


def part_2(pair_assignments: list[str]) -> int:
    pair_ranges = [_get_elf_pair_ranges(assignment) for assignment in pair_assignments]
    return sum(_ranges_overlap(a, b) for a, b in pair_ranges)


if __name__ == "__main__":
    pair_assignments = lines_in_file(Path("input.txt"))
    print(part_1(pair_assignments))
    print(part_2(pair_assignments))

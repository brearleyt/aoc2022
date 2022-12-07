import re
from collections import defaultdict
from pathlib import Path

from solutions.utils.input import lines_in_file


def get_path_name(dir_path: list[str]) -> str:
    if len(dir_path) == 1:
        return "/"
    return "/".join(dir_path)


def get_directory_sizes(terminal_lines: list[str]) -> dict[str, int]:
    sizes: dict[str, int] = defaultdict(int)

    dir_path: list[str] = []
    for line in terminal_lines:
        if match := re.match(r"\$ cd (?P<dir_name>.+)", line):
            match match["dir_name"].lstrip("/"):
                case "..":
                    dir_path.pop()
                case dir_name:
                    dir_path.append(dir_name)
        elif match := re.match(r"(?P<size>\d+) .+", line):
            dir_size = int(match["size"])
            for i in range(1, len(dir_path) + 1):
                dir_name = get_path_name(dir_path[:i])
                sizes[dir_name] += dir_size

    return sizes


def part_1(terminal_lines: list[str]) -> int:
    dir_sizes = get_directory_sizes(terminal_lines)
    return sum(size for size in dir_sizes.values() if size <= 100000)


def part_2(terminal_lines: list[str]) -> int:
    dir_sizes = get_directory_sizes(terminal_lines)
    free_space = 70000000 - dir_sizes["/"]
    required_space = 30000000 - free_space
    return min(size for size in dir_sizes.values() if size >= required_space)


if __name__ == "__main__":
    terminal_lines = lines_in_file(Path("input.txt"))
    print(part_1(terminal_lines))
    print(part_2(terminal_lines))

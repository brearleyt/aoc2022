from pathlib import Path
from typing import Optional

from solutions.utils.input import lines_in_file


def start_of_message_index(
    datastream: str, start_of_packet_width: int
) -> Optional[int]:
    max_index = max(0, len(datastream) - start_of_packet_width)
    for i in range(max_index):
        window_end = i + start_of_packet_width

        window = datastream[i:window_end]
        chars_in_windows = set(window)

        if len(chars_in_windows) == start_of_packet_width:
            return window_end
    return None


def part_1(datastream: str) -> int:
    index = start_of_message_index(datastream, 4)
    assert index is not None
    return index


def part_2(datastream: str) -> int:
    index = start_of_message_index(datastream, 14)
    assert index is not None
    return index


if __name__ == "__main__":
    datastream = lines_in_file(Path("input.txt"))[0]
    print(part_1(datastream))
    print(part_2(datastream))

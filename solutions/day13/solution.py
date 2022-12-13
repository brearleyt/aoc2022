import dataclasses
import itertools
from functools import reduce
from itertools import zip_longest
from pathlib import Path
from typing import Any, Optional

from solutions.utils.input import lines_in_file

NestedPacketContents = list[int] | list["NestedPacketContents"]
PacketContents = int | NestedPacketContents


@dataclasses.dataclass(frozen=True)
class Packet:
    contents: NestedPacketContents

    @classmethod
    def from_pair_def(cls, pair_def: str) -> "Packet":
        # I beg forgiveness for my sins
        return cls(eval(pair_def))  # pylint: disable=eval-used

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Packet):
            raise TypeError()
        order = self._compare_contents(self.contents, other.contents)
        return order is None or order

    def _compare_contents(
        self, this: NestedPacketContents, that: NestedPacketContents
    ) -> Optional[bool]:
        for left, right in zip_longest(this, that):
            if left is None:
                return True

            if right is None:
                return False

            if nested_lists := self._nest_lists_if_required(left, right):
                l, r = nested_lists  # pylint: disable=invalid-name
                if (is_lt := self._compare_contents(l, r)) is not None:
                    return is_lt
                continue

            assert isinstance(left, int)
            assert isinstance(right, int)

            if left == right:
                continue

            return left < right
        return None

    @staticmethod
    def _nest_lists_if_required(
        left: PacketContents, right: PacketContents
    ) -> Optional[tuple[NestedPacketContents, NestedPacketContents]]:
        if isinstance(left, list) and isinstance(right, list):
            return left, right
        if isinstance(left, int) and isinstance(right, list):
            return [left], right
        if isinstance(left, list) and isinstance(right, int):
            return left, [right]
        return None


def part_1(pairs_def: list[str]) -> int:
    pairs = (
        (Packet.from_pair_def(pairs_def[i]), Packet.from_pair_def(pairs_def[i + 1]))
        for i in range(0, len(pairs_def), 3)
    )
    return sum(
        i
        for i, (packet_a, packet_b) in enumerate(pairs, start=1)
        if packet_a < packet_b
    )


def part_2(pairs: list[str]) -> int:
    packets = (Packet.from_pair_def(packet) for packet in pairs if packet)
    dividers = (Packet.from_pair_def("[[2]]"), Packet.from_pair_def("[[6]]"))
    ordered_packets = sorted(itertools.chain(packets, dividers))
    return reduce(
        lambda a, b: a * b,
        (i for i, packet in enumerate(ordered_packets, start=1) if packet in dividers),
    )


if __name__ == "__main__":
    pairs = lines_in_file(Path("input.txt"))
    print(part_1(pairs))
    print(part_2(pairs))

import dataclasses
import heapq
import math
import re
from collections import deque
from functools import reduce
from pathlib import Path
from typing import Callable, Iterator

from solutions.utils.input import lines_in_file


def _build_op(operator: str, operand: str) -> Callable[[int], int]:
    def multiply(score: int) -> int:
        if operand == "old":
            return score * score
        return score * int(operand)

    def add(score: int) -> int:
        if operand == "old":
            return score + score
        return score + int(operand)

    match operator:
        case "*":
            return multiply
        case "+":
            return add
        case _:
            raise ValueError(f"Unexpected operator {operator}")


@dataclasses.dataclass()
class Monkey:
    id_: int
    inspected_count: int
    items: deque[int]
    operator: Callable[[int], int]
    divisible_by: int
    throw_to_if_divisible: int
    throw_to_if_not_divisible: int

    @classmethod
    def create(cls, monkey_notes: Iterator[str]) -> "Monkey":
        id_ = re.match(r"Monkey (\d+):", next(monkey_notes))
        assert id_

        starting_items = re.findall(r"(\d+)", next(monkey_notes))
        assert starting_items

        operation = re.search(r"Operation: new = old (.) (.+)", next(monkey_notes))
        assert operation

        test = re.search(r"Test: divisible by (\d+)", next(monkey_notes))
        assert test

        if_true = re.search(r"If true: throw to monkey (\d+)", next(monkey_notes))
        assert if_true

        if_false = re.search(r"If false: throw to monkey (\d+)", next(monkey_notes))
        assert if_false

        return cls(
            id_=int(id_.group(1)),
            inspected_count=0,
            items=deque(int(x) for x in starting_items),
            operator=_build_op(operator=operation.group(1), operand=operation.group(2)),
            divisible_by=int(test.group(1)),
            throw_to_if_divisible=int(if_true.group(1)),
            throw_to_if_not_divisible=int(if_false.group(1)),
        )

    def run(self, worry_reducer: Callable[[int], int]) -> list[tuple[int, int]]:
        results = []

        while self.items:
            self.inspected_count += 1
            score = worry_reducer(self.operator(self.items.pop()))
            next_id = (
                self.throw_to_if_divisible
                if score % self.divisible_by == 0
                else self.throw_to_if_not_divisible
            )
            results.append((score, next_id))

        return results


def get_monkeys(monkey_notes: list[str]) -> dict[int, Monkey]:
    notes = iter(monkey_notes)

    monkeys = {}
    while True:
        monkey = Monkey.create(notes)
        monkeys[monkey.id_] = monkey
        try:
            next(notes)
        except StopIteration:
            break

    return monkeys


def monkey_business_level(
    monkeys: dict[int, Monkey],
    number_of_rounds: int,
    worry_reducer: Callable[[int], int],
) -> int:
    for _ in range(number_of_rounds):
        for monkey in monkeys.values():
            for score, next_id in monkey.run(worry_reducer):
                monkeys[next_id].items.append(score)

    two_largest = heapq.nlargest(
        2, (monkey.inspected_count for monkey in monkeys.values())
    )
    return reduce(lambda a, b: a * b, two_largest)


def part_1(monkey_notes: list[str]) -> int:
    monkeys = get_monkeys(monkey_notes)

    def worry_reducer(level: int) -> int:
        return level // 3

    return monkey_business_level(monkeys, 20, worry_reducer)


def part_2(monkey_notes: list[str]) -> int:
    monkeys = get_monkeys(monkey_notes)

    # I had to cheat to get this :(
    lcm = math.lcm(*[m.divisible_by for m in monkeys.values()])

    def worry_reducer(y: int) -> int:
        return y % lcm

    return monkey_business_level(monkeys, 10000, worry_reducer)


if __name__ == "__main__":
    monkey_notes = lines_in_file(Path("input.txt"))
    print(part_1(monkey_notes))
    print(part_2(monkey_notes))

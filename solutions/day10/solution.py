from pathlib import Path
from typing import Optional

from collections_extended import RangeMap  # type: ignore

from solutions.utils.input import chunked_iter, lines_in_file


def command_and_args(program_command: str) -> tuple[str, Optional[tuple[str, ...]]]:
    command_and_args = program_command.split(" ")

    if len(command_and_args) == 1:
        return command_and_args[0], None

    return command_and_args[0], tuple(command_and_args[1:])


def get_program_state(program_commands: list[str]) -> RangeMap:
    program_state = RangeMap()

    tick = 1
    register_value = 1
    for command in program_commands:
        command, args = command_and_args(command)
        match command:
            case "noop":
                tick += 1
            case "addx":
                assert args
                tick += 2
                program_state[program_state.end or 0 : tick] = register_value
                register_value += int(args[0])
            case _:
                raise ValueError(f"Unrecognised instruction {command}")

    program_state[program_state.end or 0 : tick] = register_value

    return program_state


def signal_strength(program_state: RangeMap, tick: int) -> int:
    state: int = program_state[tick]
    return state * tick


def pixel_state(row: int, index: int, state: RangeMap) -> str:
    tick = (row * 40) + index + 1
    if index - 1 <= state[tick] <= index + 1:
        return "#"
    return "."


def part_1(program_commands: list[str]) -> int:
    state = get_program_state(program_commands)
    return sum(signal_strength(state, i) for i in range(20, state.end, 40))


def part_2(program_commands: list[str]) -> list[str]:
    state = get_program_state(program_commands)
    pixel_states = [
        pixel_state(row, index, state) for row in range(6) for index in range(40)
    ]
    rows = ["".join(row) for row in chunked_iter(pixel_states, 40)]
    for row in rows:
        print(row)
    return rows


if __name__ == "__main__":
    program_commands = lines_in_file(Path("input.txt"))
    print(part_1(program_commands))
    print(part_2(program_commands))

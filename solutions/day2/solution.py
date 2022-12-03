from enum import Enum, auto, unique
from pathlib import Path

from solutions.utils.input import lines_in_file


@unique
class Result(Enum):
    WIN = auto()
    DRAW = auto()
    LOSE = auto()

    @classmethod
    def from_code(cls, code: str) -> "Result":
        return {
            "X": Result.LOSE,
            "Y": Result.DRAW,
            "Z": Result.WIN,
        }[code]

    @property
    def score(self) -> int:
        return {
            Result.WIN: 6,
            Result.DRAW: 3,
            Result.LOSE: 0,
        }[self]


@unique
class Move(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

    @classmethod
    def from_code(cls, code: str) -> "Move":
        match code:
            case "A" | "X":
                return Move.ROCK
            case "B" | "Y":
                return Move.PAPER
            case "C" | "Z":
                return Move.SCISSORS
            case unexpected_:
                raise ValueError(f"Unexpected code {unexpected_}")

    @property
    def score(self) -> int:
        return {
            Move.ROCK: 1,
            Move.PAPER: 2,
            Move.SCISSORS: 3,
        }[self]

    @property
    def beats(self) -> "Move":
        return {
            Move.ROCK: Move.SCISSORS,
            Move.PAPER: Move.ROCK,
            Move.SCISSORS: Move.PAPER,
        }[self]

    @property
    def loses_to(self) -> "Move":
        return {
            Move.ROCK: Move.PAPER,
            Move.PAPER: Move.SCISSORS,
            Move.SCISSORS: Move.ROCK,
        }[self]


def play_game(self: Move, opponents: Move) -> Result:
    if self.beats == opponents:
        return Result.WIN
    if self == opponents:
        return Result.DRAW
    return Result.LOSE


def move_for_desired_result(opponents_move: Move, desired_result: Result) -> Move:
    match desired_result:
        case Result.WIN:
            return opponents_move.loses_to
        case Result.DRAW:
            return opponents_move
        case Result.LOSE:
            return opponents_move.beats


def _score_of_games(moves: list[tuple[Move, Move]]) -> int:
    return sum(
        (mine.score + play_game(mine, opponents).score) for opponents, mine in moves
    )


def _moves_from_game_codes(game: str) -> tuple[Move, Move]:
    opponents, mine = game.split(" ")
    return Move.from_code(opponents), Move.from_code(mine)


def _opponents_move_and_desired_result_from_game_codes(
    game: str,
) -> tuple[Move, Result]:
    opponents, mine = game.split(" ")
    return Move.from_code(opponents), Result.from_code(mine)


def part_1(games: list[str]) -> int:
    game_moves = [_moves_from_game_codes(game) for game in games]
    return _score_of_games(game_moves)


def part_2(games: list[str]) -> int:
    moves_and_results = [
        _opponents_move_and_desired_result_from_game_codes(game) for game in games
    ]
    game_moves = [
        (opponents_move, move_for_desired_result(opponents_move, desired_result))
        for opponents_move, desired_result in moves_and_results
    ]
    return _score_of_games(game_moves)


if __name__ == "__main__":
    games = lines_in_file(Path("input.txt"))
    print(part_1(games))
    print(part_2(games))

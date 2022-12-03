from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    lines = s.splitlines()

    score = 0
    for line in lines:
        opponent, you = line.split()

        if you == "X":
            # Opponent plays  Rock Paper Scissors
            # To Lose, play:   P    R    S
            score += 0 + 1 + ["B", "C", "A"].index(opponent)
        elif you == "Y":
            # To Draw, play:   R    P    S
            score += 3 + 1 + ["A", "B", "C"].index(opponent)
        elif you == "Z":
            # To Win, play:    S    R    P
            score += 6 + 1 + ["C", "A", "B"].index(opponent)
        else:
            raise AssertionError(you)

    return score


INPUT_S = """\
A Y
B X
C Z
"""
EXPECTED = 12


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple, TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

Stack: TypeAlias = list[str | None]


def parse_row(line: str) -> Stack:
    """Parses each row of crates to the crate digit, or Nones for blanks."""
    crates: Stack = []
    for index in range(1, len(line), 4):
        char = line[index]
        if char == " ":
            crates.append(None)
        else:
            crates.append(char)

    return crates


class Command(NamedTuple):
    creates: int
    start: int
    end: int


def parse_command(line: str) -> Command:
    count, start, end = [int(i) for i in line.split() if i.isdigit()]
    return Command(count, start, end)


def rearrange(stacks: list[Stack], commands: list[Command]) -> None:
    for command in commands:
        count, start, end = command

        top = []
        for _ in range(count):
            top.append(stacks[start - 1].pop())

        for item in reversed(top):
            stacks[end - 1].append(item)


def compute(s: str) -> int:
    crate_rows: list[list[str | None]] = []
    commands: list[Command] = []

    lines = s.splitlines()
    for line in lines:
        if line.lstrip().startswith("["):
            crate_rows.append(parse_row(line))
        elif line.startswith("move"):
            commands.append(parse_command(line))

    stacks: list[Stack] = [[] for _ in range(len(crate_rows[0]))]
    for row in reversed(crate_rows):
        for index, crate in enumerate(row):
            if crate is not None:
                stacks[index].append(crate)

    rearrange(stacks, commands)

    return "".join(stack[-1] for stack in stacks)


INPUT_S = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
EXPECTED = "MCD"


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: str) -> None:
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

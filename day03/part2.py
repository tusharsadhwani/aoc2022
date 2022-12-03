from __future__ import annotations

import argparse
import os.path
import string
from collections import deque

import pytest
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    lines = deque(s.splitlines())
    result = 0

    while lines:
        line1, line2, line3 = lines.popleft(), lines.popleft(), lines.popleft()
        common = set(line1).intersection(set(line2)).intersection(set(line3)).pop()

        if common.islower():
            priority = 1 + string.ascii_lowercase.index(common)
        else:
            priority = 27 + string.ascii_uppercase.index(common)

        result += priority

    return result


INPUT_S = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
EXPECTED = 70


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

from __future__ import annotations

import argparse
from collections import deque
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    chars = deque(maxlen=14)
    for index, char in enumerate(s):
        chars.append(char)
        if len(chars) == 14 and len(set(chars)) == 14:
            return index + 1


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ),
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

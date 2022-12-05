from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def fully_contained(s1, e1, s2, e2):
    return s1 >= s2 and e1 <= e2


def compute(s: str) -> int:
    lines = s.splitlines()

    count = 0
    for line in lines:
        start1, end1, start2, end2 = [
            int(x) for r in line.split(",") for x in r.split("-")
        ]
        if fully_contained(start1, end1, start2, end2) or fully_contained(
            start2,
            end2,
            start1,
            end1,
        ):
            count += 1

    return count


INPUT_S = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
EXPECTED = 2


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

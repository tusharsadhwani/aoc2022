from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    score = 0
    for line in lines:
        other, you = line.split()
        score += 1 + ['X', 'Y', 'Z'].index(you)
        if you == 'X':
            score += 3 * ['B', 'A', 'C'].index(other)
        elif you == 'Y':
            score += 3 * ['C', 'B', 'A'].index(other)
        elif you == 'Z':
            score += 3 * ['A', 'C', 'B'].index(other)
        else:
            raise AssertionError(you)


    return score


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

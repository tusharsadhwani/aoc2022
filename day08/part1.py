from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def is_visible(grid, row, col):
    rows = len(grid)
    cols = len(grid[0])

    if row == 0 or row == rows - 1:
        return True

    if col == 0 or col == cols - 1:
        return True

    cell = grid[row][col]

    # left
    if all(grid[row][i] < cell for i in range(col - 1, -1, -1)):
        return True
    # right
    if all(grid[row][i] < cell for i in range(col + 1, cols)):
        return True

    # up
    if all(grid[i][col] < cell for i in range(row - 1, -1, -1)):
        return True
    # down
    if all(grid[i][col] < cell for i in range(row + 1, rows)):
        return True

    return False


def compute(s: str) -> int:
    grid = [[int(cell) for cell in row] for row in s.splitlines()]

    count = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if is_visible(grid, row, col):
                count += 1

    return count


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 21


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

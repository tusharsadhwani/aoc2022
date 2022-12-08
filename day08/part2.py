from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def scenic_score(grid, row, col):
    rows = len(grid)
    cols = len(grid[0])

    if row == 0 or row == rows - 1:
        return 0

    if col == 0 or col == cols - 1:
        return 0

    cell = grid[row][col]

    score = 1
    # left
    count = 0
    for i in range(col - 1, -1, -1):
        count += 1
        if grid[row][i] >= cell:
            break

    score *= count
    # right
    count = 0
    for i in range(col + 1, cols):
        count += 1
        if grid[row][i] >= cell:
            break

    score *= count

    # up
    count = 0
    for i in range(row - 1, -1, -1):
        count += 1
        if grid[i][col] >= cell:
            break

    score *= count
    # down
    count = 0
    for i in range(row + 1, rows):
        count += 1
        if grid[i][col] >= cell:
            break

    score *= count

    return score


def compute(s: str) -> int:
    grid = [[int(cell) for cell in row] for row in s.splitlines()]

    max_score = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            score = scenic_score(grid, row, col)
            if score > max_score:
                max_score = score

    return max_score


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 8


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

from __future__ import annotations

import argparse
from collections import defaultdict
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    lines = s.splitlines()
    dir_contents = defaultdict(list)

    file_sizes = {}
    dir_sizes = defaultdict(int)

    index = 0
    current_path = []
    while index < len(lines):
        line = lines[index]
        index += 1

        if not line.startswith("$"):
            raise AssertionError(f"Expected command on line {index+1}, got {line}")

        command = line[2:].split()
        match command:
            case ["cd", directory]:
                if directory == "/":
                    current_path = []
                elif directory == "..":
                    current_path.pop()
                else:
                    current_path.append(directory)

            case ["ls"]:
                # parse files and directories
                while index < len(lines):
                    line = lines[index]
                    if line.startswith("$"):
                        break
                    a, b = line.split()

                    if a == "dir":
                        dir_name = b
                        dir_contents[tuple(current_path)].append(dir_name)

                    else:
                        file_size, file_name = int(a), b
                        dir_contents[tuple(current_path)].append(file_name)

                        file_path = tuple([*current_path, file_name])
                        assert file_path not in file_sizes
                        file_sizes[file_path] = file_size

                        # recursively save file size up the directory
                        for i in range(len(current_path), -1, -1):
                            ancestor_path = tuple(current_path[:i])
                            dir_sizes[ancestor_path] += file_size

                    index += 1

    total_used = dir_sizes[()]
    unused = 70000000 - total_used
    needed = 30000000 - unused

    smallest_big_enough = float("inf")
    for dir_size in dir_sizes.values():
        if dir_size > needed and dir_size < smallest_big_enough:
            smallest_big_enough = dir_size

    return smallest_big_enough


INPUT_S = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
EXPECTED = 24933642


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

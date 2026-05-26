#!/usr/bin/env python3

def read_hex_map() -> tuple:
    int_map: list[list[int]] = []
    row: list[int] = []
    output_file: str = "tests/output_file.txt"
    # output_file: str = "output_file.txt"
    entry: tuple
    exit: tuple
    path: str

    with open(output_file, "r") as maze_file:
        for line in maze_file:
            if line == "\n":
                break
            row = [int(char, 16) for char in line.strip()]
            int_map.append(row)
        entry = tuple(int(item) for item in
                      maze_file.readline().strip().split(","))
        exit = tuple(int(item) for item in
                     maze_file.readline().strip().split(","))
        path = maze_file.readline().strip()

    return (int_map, entry, exit, path)

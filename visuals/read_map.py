#!/usr/bin/env python3

def read_hex_map() -> tuple:
    """Reads the output.txt for information to create the map and the path

    Returns:
        int_map: The map filled with ints indicating the wall structure of
        each cell.
        path: The string or directional instructions
    """
    int_map: list[list[int]] = []
    row: list[int] = []
    output_file: str = "tests/output_file.txt"
    # output_file: str = "output_file.txt"
    path: str = ""

    with open(output_file, "r") as maze_file:
        for line in maze_file:
            if line == "\n":
                break
            row = [int(char, 16) for char in line.strip()]
            int_map.append(row)
        maze_file.readline().strip()
        maze_file.readline().strip()
        path = maze_file.readline().strip()
    return (int_map, path)

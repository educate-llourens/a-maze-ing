#!/usr/bin/env python3

from visuals.display_errors import DisplayError
from visuals.read_map import read_hex_map
# from mlx import Mlx

# Binary values:
#   A  | 1111 = 15
#   N  | 0111 = 7
#   E  | 1011 = 11
#   S  | 1101 = 13
#   W  | 1110 = 14
#   NE | 0011 = 3
#   NS | 0101 = 5
#   NW | 0110 = 6
#   SW | 1100 = 12
#   SE | 1001 = 9
#   EW | 1010 = 10


# def mlx_display(list: int) -> None:
#     mlx: Mlx = Mlx()
#     connection_ptr = mlx.mlx_init()


def read_hex_map(configs: dict) -> list[str]:
    str_map: list[str] = []
    row: str = ""
    output_file: str = "tests/output_file.txt"
    # output_file: str = "output_file.txt"

    with open(output_file, "r") as maze_file:
        for line in maze_file:
            row = maze_file.readline()
            str_map.append(row)
    return str_map


def display_maze(configs: dict) -> None:
    map_rows: list[str]

    map_rows = read_hex_map(configs)
    # Convert to directions
    # mlx_display(map_rows)
    print(map_rows)

#!/usr/bin/env python3

from visuals.display_errors import DisplayError
from visuals.read_map import read_hex_map
from parsing.parsing_errors import FileError
from enum import Enum
# from mlx import Mlx

# W S E N

# Binary values:
#   A  | 1111 = 15
#   N  | 1110 = 14
#   E  | 1101 = 13
#   S  | 1011 = 11
#   W  | 0111 = 7
#   NE | 1100 = 12
#   NS | 1010 = 10
#   NW | 0110 = 6
#   SW | 0011 = 3
#   SE | 1001 = 9
#   EW | 0101 = 5


# class Directions(Enum):
#     ALL = 15
#     N = 14
#     E = 13
#     S = 11
#     W = 7
#     NE = 12
#     NS = 10
#     NW = 6
#     SW = 3
#     SE = 9
#     EW = 5


# def mlx_display(list: int) -> None:
#     mlx: Mlx = Mlx()
#     connection_ptr = mlx.mlx_init()


def display_maze(configs: dict) -> None:
    maze: list[list[int]] = []
    path: str = ""

    try:
        maze, path = read_hex_map()
    except Exception as msg:
        raise FileError(msg)
    # mlx_display(map_rows)

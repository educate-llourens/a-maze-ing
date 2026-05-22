#!/usr/bin/env python3

from visuals.display_errors import DisplayError
from visuals.read_map import read_hex_map
import ctypes


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


def mlx_display(list: int) -> None:
    mlx: ctypes.CDLL = ctypes.CDLL("libmlx.so")

    

def display_map() -> None:
    map_rows: list[str]

    create_map()
    map_rows = read_hex_map()
    # Convert to directions
    mlx_display(map_rows)

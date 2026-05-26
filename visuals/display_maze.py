#!/usr/bin/env python3

from visuals.display_errors import DisplayError
from visuals.read_map import read_hex_map
from parsing.parsing_errors import FileError, ConfigError
from typing import Any
# from enum import Enum
from mlx import Mlx
import signal

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


def mlx_display(maze: list[list[int]], configs: dict) -> None:
    mlx: Mlx = Mlx()
    window_ptr: Any
    window_width: int
    window_height: int
    window_ptr: Any

    try:
        window_width = configs["WIDTH"] * 2
        window_height = configs["HEIGHT"] * 2
    except KeyError:
        raise ConfigError("No 'WIDTH or 'HEIGHT' key in config for mlx")
    initialised_mlx = mlx.mlx_init()
    if initialised_mlx is None:
        raise DisplayError("Unable to initialise mlx")
    window_ptr = mlx.mlx_new_window(initialised_mlx, window_width,
                                    window_height, "a-maze-ing")
    signal.signal(signal.SIGINT, mlx.mlx_loop_exit(initialised_mlx))
    mlx.mlx_loop(initialised_mlx)
    mlx.mlx_destroy_window(initialised_mlx, window_ptr)


def display_maze(configs: dict) -> None:
    maze: list[list[int]] = []
    path: str = ""

    try:
        maze, path = read_hex_map()
    except Exception as msg:
        raise FileError(msg)
    mlx_display(maze, configs)

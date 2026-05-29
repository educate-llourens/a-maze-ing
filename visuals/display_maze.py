#!/usr/bin/env python3

from visuals.display_errors import DisplayError
from visuals.read_map import read_hex_map
from parsing.parsing_errors import FileError, ConfigError
from typing import Any
# from enum import Enum
from mlx import Mlx
import signal
import os

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


class MlxData:
    def __init__(self):
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        if self.mlx_ptr is None:
            raise DisplayError("Unable to initialise mlx")

class WindowData:
    def __init__(self, configs: dict, mlx: MlxData):
        try:
            self.width = configs["WIDTH"] * 32
            self.height = configs["HEIGHT"] * 32
        except KeyError:
            raise ConfigError("No 'WIDTH or 'HEIGHT' key in "
                                "config for mlx")
        self.window_ptr = mlx.mlx.mlx_new_window(mlx.mlx_ptr, self.width,
                                    self.height, "a-maze-ing")

class ImageData:
    def __init__(self, mlx: MlxData, window: WindowData):
        self.image_ptr = mlx.mlx.mlx_new_image(mlx.mlx_ptr, window.width,
                                               window.height)


def create_image(image: ImageData, mlx: MlxData, window: WindowData) -> None:
    y = 100
    while y < 300:
        x = 100
        while x < 400:
            mlx.mlx.mlx_pixel_put(mlx.mlx_ptr, window.window_ptr,
                                  x, y, 0xFFFFFF)
            x += 1
        y += 1


def mlx_display(maze: list[list[int]], configs: dict) -> None:
    mlx: MlxData = MlxData()
    window = WindowData(configs, mlx)
#     # image = ImageData(mlx, window)

#     # create_image(image, mlx, window)
#     def draw(param):
#         y = 100
#         while y < 300:
#             x = 100
#             while x < 400:
#                 mlx.mlx.mlx_pixel_put(mlx.mlx_ptr, window.window_ptr, x, y, 0xFFFFFF)
#                 x += 1
#             y += 1

    try:
        mlx.mlx.mlx_loop(mlx.mlx_ptr)
    except KeyboardInterrupt:
        print("Error: Keyboard input interrupted the program. Shuttingdown")
        signal.signal(signal.SIGINT, os._exit(0))
#     mlx.mlx.mlx_destroy_window(mlx.mlx_ptr, window.window_ptr)


def display_maze(configs: dict) -> None:
    maze: list[list[int]] = []
    path: str = ""

    try:
        maze, path = read_hex_map()
    except Exception as msg:
        raise FileError(msg)
    mlx_display(maze, configs)

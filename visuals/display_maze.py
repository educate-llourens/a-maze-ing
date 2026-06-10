#!/usr/bin/env python3

from visuals.display_errors import DisplayError
from visuals.read_map import read_hex_map
from parsing.parsing_errors import FileError
from mlx import Mlx


def mlx_display(maze: list[list[int]], configs: dict) -> None:
    mlx: Mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    window_ptr = mlx.mlx_new_window(mlx_ptr, 500,
                                    500, "A-maze-ing")
    png_to_window = mlx.mlx_png_file_to_image(mlx_ptr,
                                              "./visuals/assets/brick_wall.png")
    image_ptr, image_width, image_height = png_to_window
    mlx.mlx_put_image_to_window(mlx_ptr, window_ptr, image_ptr, 15, 15)
    mlx.mlx_hook(window_ptr, 33, 0, lambda any: mlx.mlx_loop_exit(mlx_ptr),
                 None)
    mlx.mlx_loop(mlx_ptr)


def display_maze(configs: dict) -> None:
    maze: list[list[int]] = []
    path: str = ""

    try:
        maze, path = read_hex_map()
    except Exception as msg:
        raise FileError(msg)
    try:
        mlx_display(maze, configs)
    except Exception as msg:
        raise DisplayError(msg)

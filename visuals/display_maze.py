#!/usr/bin/env python3

from visuals.display_errors import DisplayError
from visuals.read_map import read_hex_map
from parsing.parsing_errors import FileError
from mlx import Mlx


def mlx_display(maze: list[list[int]], configs: dict, path: str) -> None:
    mlx: Mlx = Mlx()
    mlx_ptr = mlx.mlx_init()

    TILE = 48
    WALL = 48
    STEP = TILE + WALL

    rows = len(maze)
    cols = max(len(row) for row in maze)

    win_w = cols * STEP + WALL
    win_h = rows * STEP + WALL

    window_ptr = mlx.mlx_new_window(mlx_ptr, win_w, win_h, "A-maze-ing")

    png = mlx.mlx_png_file_to_image(mlx_ptr, "./visuals/assets/brick_wall.png")
    image_ptr, image_width, image_height = png

    NORTH = 1
    SOUTH = 2
    EAST  = 4
    WEST  = 8

    def fill_wall(px, py, w, h):
        for ty in range(0, h, image_height):
            for tx in range(0, w, image_width):
                mlx.mlx_put_image_to_window(mlx_ptr, window_ptr, image_ptr,
                                            px + tx, py + ty)

    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):  # use row, not cols
            cx = col_idx * STEP
            cy = row_idx * STEP

            fill_wall(cx, cy, WALL, WALL)

            if cell & NORTH:
                fill_wall(cx + WALL, cy, TILE, WALL)

            if cell & WEST:
                fill_wall(cx, cy + WALL, WALL, TILE)

    # Right edge — use actual row length, not global cols
    for row_idx, row in enumerate(maze):
        cx = len(row) * STEP
        cy = row_idx * STEP
        fill_wall(cx, cy, WALL, WALL)
        if row[-1] & EAST:
            fill_wall(cx, cy + WALL, WALL, TILE)

    # Bottom edge
    bottom_row = maze[-1]
    cy = rows * STEP
    for col_idx, cell in enumerate(bottom_row):
        cx = col_idx * STEP
        fill_wall(cx, cy, WALL, WALL)
        if cell & SOUTH:
            fill_wall(cx + WALL, cy, TILE, WALL)

    # Bottom-right corner
    fill_wall(len(maze[-1]) * STEP, rows * STEP, WALL, WALL)

    mlx.mlx_hook(window_ptr, 33, 0, lambda any: mlx.mlx_loop_exit(mlx_ptr), None)
    mlx.mlx_loop(mlx_ptr)


# def mlx_display(maze: list[list[int]], configs: dict, path: str) -> None:
#     mlx: Mlx = Mlx()
#     mlx_ptr = mlx.mlx_init()
#     window_ptr = mlx.mlx_new_window(mlx_ptr, 500,
#                                     500, "A-maze-ing")
#     png_to_window = mlx.mlx_png_file_to_image(mlx_ptr,
#                                               "./visuals/assets/brick_wall.png")
#     image_ptr, image_width, image_height = png_to_window
#     mlx.mlx_put_image_to_window(mlx_ptr, window_ptr, image_ptr, 15, 15)
#     mlx.mlx_hook(window_ptr, 33, 0, lambda any: mlx.mlx_loop_exit(mlx_ptr),
#                  None)
#     mlx.mlx_loop(mlx_ptr)


def display_maze(configs: dict) -> None:
    maze: list[list[int]] = []
    path: str = ""

    try:
        maze, path = read_hex_map()
    except Exception as msg:
        raise FileError(msg)
    try:
        mlx_display(maze, configs, path)
    except Exception as msg:
        raise DisplayError(msg)

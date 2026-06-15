#!/usr/bin/env python3

from visuals.display_classes import DrawInfo, Direction
from mlx import Mlx


def has_north_wall(cell_value: int) -> bool:
    return bool(cell_value & Direction.NORTH.value)


def has_west_wall(cell_value: int) -> bool:
    return bool(cell_value & Direction.WEST.value)


def draw_maze(drawing: DrawInfo, mlx: Mlx, mlx_ptr) -> None:
    def fill_wall(start_x: int, start_y: int, width: int, height: int) -> None:
        for offset_y in range(0, height, image.height):
            for offset_x in range(0, width, image.width):
                mlx.mlx_put_image_to_window(
                    mlx_ptr,
                    window_ptr,
                    image.ptr,
                    start_x + offset_x,
                    start_y + offset_y,
                )

    def draw_top_border():
        top_y = 0
        for col_index in range(cols):
            col_x = col_index * passage
            fill_wall(col_x, top_y, wall, wall)
            fill_wall(col_x + wall, top_y, inner, wall)
        fill_wall(cols * passage, top_y, wall, wall)

    def draw_left_border():
        left_x = 0
        for row_index in range(rows):
            row_y = row_index * passage
            fill_wall(left_x, row_y, wall, wall)
            fill_wall(left_x, row_y + wall, wall, inner)
        fill_wall(left_x, rows * passage, wall, wall)

    def draw_internal_walls():
        for row_index, cell_list in enumerate(drawing.maze):
            row_y = row_index * passage
            for col_index, cell_value in enumerate(cell_list):
                col_x = col_index * passage

                # Corner joint at the top-left of the cell
                fill_wall(col_x, row_y, wall, wall)

                # Horizontal segment across the top of the cell interior
                if has_north_wall(cell_value):
                    fill_wall(col_x + wall, row_y, inner, wall)

                # Vertical segment down the left of the cell interior
                if has_west_wall(cell_value):
                    fill_wall(col_x, row_y + wall, wall, inner)

    def draw_right_border():
        right_x = cols * passage
        for row_index in range(rows):
            row_y = row_index * passage
            fill_wall(right_x, row_y, wall, wall)
            fill_wall(right_x, row_y + wall, wall, inner)
        fill_wall(right_x, rows * passage, wall, wall)

    def draw_bottom_border():
        bottom_y = rows * passage
        for col_index in range(cols):
            col_x = col_index * passage
            fill_wall(col_x, bottom_y, wall, wall)
            fill_wall(col_x + wall, bottom_y, inner, wall)
        fill_wall(cols * passage, bottom_y, wall, wall)

    tile = drawing.tile
    image = drawing.image
    window_ptr = drawing.window.ptr

    wall = tile.wall
    inner = tile.tile
    passage = tile.passage
    rows = tile.rows
    cols = tile.cols

    draw_top_border()
    draw_left_border()
    draw_internal_walls()
    draw_right_border()
    draw_bottom_border()




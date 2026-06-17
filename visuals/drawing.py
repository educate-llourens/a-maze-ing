#!/usr/bin/env python3

from visuals.display_classes import DrawInfo, Direction
from mlx import Mlx


class DrawingData:
    def __init__(self, drawing: DrawInfo, mlx, mlx_ptr) -> None:
        self.tile = drawing.tile
        self.image = drawing.image
        self.window_ptr = drawing.window.ptr
        self.wall = self.tile.wall
        self.inner = self.tile.tile
        self.passage = self.tile.passage
        self.rows = self.tile.rows
        self.cols = self.tile.cols
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.maze = drawing.maze


def has_north_wall(cell_value: int) -> bool:
    return bool(cell_value & Direction.NORTH.value)


def has_west_wall(cell_value: int) -> bool:
    return bool(cell_value & Direction.WEST.value)


def fill_wall(data: DrawingData, start_x: int, start_y: int, width: int,
              height: int) -> None:
    for offset_y in range(0, height, data.image.wall_height):
        for offset_x in range(0, width, data.image.wall_width):
            data.mlx.mlx_put_image_to_window(
                data.mlx_ptr,
                data.window_ptr,
                data.image.wall_ptr,
                start_x + offset_x,
                start_y + offset_y,
            )


def draw_top_border(data: DrawingData):
    top_y = 0
    for col_index in range(data.cols):
        col_x = col_index * data.passage
        fill_wall(data, col_x, top_y, data.wall, data.wall)
        fill_wall(data, col_x + data.wall, top_y, data.inner, data.wall)
    fill_wall(data, data.cols * data.passage, top_y, data.wall, data.wall)


def draw_left_border(data: DrawingData):
    left_x = 0
    for row_index in range(data.rows):
        row_y = row_index * data.passage
        fill_wall(data, left_x, row_y, data.wall, data.wall)
        fill_wall(data, left_x, row_y + data.wall, data.wall, data.inner)
    fill_wall(data, left_x, data.rows * data.passage, data.wall, data.wall)


def draw_internal_walls(data: DrawingData):
    for row_index, cell_list in enumerate(data.maze):
        row_y = row_index * data.passage
        for col_index, cell_value in enumerate(cell_list):
            col_x = col_index * data.passage

            # Corner joint at the top-left of the cell
            fill_wall(data, col_x, row_y, data.wall, data.wall)

            # Horizontal segment across the top of the cell interior
            if has_north_wall(cell_value):
                fill_wall(data, col_x + data.wall, row_y, data.inner,
                          data.wall)

            # Vertical segment down the left of the cell interior
            if has_west_wall(cell_value):
                fill_wall(data, col_x, row_y + data.wall, data.wall,
                          data.inner)


def draw_entry(data: DrawingData, drawing: DrawInfo):
    row_index, col_index = drawing.entry_coord
    col_x = col_index * data.passage
    row_y = row_index * data.passage
    data.mlx.mlx_put_image_to_window(
        data.mlx_ptr,
        data.window_ptr,
        data.image.start_ptr,
        col_x + data.wall,
        row_y + data.wall,
    )


def draw_exit(data: DrawingData, drawing: DrawInfo):
    row_index, col_index = drawing.exit_coord
    col_x = col_index * data.passage
    row_y = row_index * data.passage
    data.mlx.mlx_put_image_to_window(
        data.mlx_ptr,
        data.window_ptr,
        data.image.end_ptr,
        col_x + data.wall,
        row_y + data.wall,
    )


def draw_right_border(data: DrawingData):
    right_x = data.cols * data.passage
    for row_index in range(data.rows):
        row_y = row_index * data.passage
        fill_wall(data, right_x, row_y, data.wall, data.wall)
        fill_wall(data, right_x, row_y + data.wall, data.wall, data.inner)
    fill_wall(data, right_x, data.rows * data.passage, data.wall, data.wall)


def draw_bottom_border(data: DrawingData):
    bottom_y = data.rows * data.passage
    for col_index in range(data.cols):
        col_x = col_index * data.passage
        fill_wall(data, col_x, bottom_y, data.wall, data.wall)
        fill_wall(data, col_x + data.wall, bottom_y, data.inner, data.wall)
    fill_wall(data, data.cols * data.passage, bottom_y, data.wall, data.wall)


def draw_beginning_maze(drawing: DrawInfo, mlx: Mlx, mlx_ptr) -> None:
    data: DrawingData = DrawingData(drawing, mlx, mlx_ptr)

    draw_top_border(data)
    draw_left_border(data)
    draw_internal_walls(data)
    draw_right_border(data)
    draw_bottom_border(data)
    draw_entry(data, drawing)
    draw_exit(data, drawing)


def draw_maze(drawing: DrawInfo, mlx: Mlx, mlx_ptr, entry_coord,
              exit_coord) -> None:
    draw_beginning_maze(drawing, mlx, mlx_ptr)

#!/usr/bin/env python3

from visuals.display_classes import DrawInfo, Direction
from mlx import Mlx


def draw_maze(drawing: DrawInfo, mlx: Mlx, mlx_ptr) -> None:
    def fill_wall(start_x, start_y, width, height):
        for tile_y in range(0, height, drawing.image.height):
            for tile_x in range(0, width, drawing.image.width):
                mlx.mlx_put_image_to_window(
                    mlx_ptr, drawing.window.ptr, drawing.image.ptr,
                    start_x + tile_x, start_y + tile_y)

    for row_index, cell_list in enumerate(drawing.maze):
        for col_index, cell_value in enumerate(cell_list):
            col_x = col_index * drawing.tile.passage
            col_y = row_index * drawing.tile.passage
            fill_wall(col_x, col_y, drawing.tile.wall, drawing.tile.wall)
            if cell_value & Direction.NORTH.value:
                fill_wall(col_x + drawing.tile.wall, col_y,
                          drawing.tile.tile, drawing.tile.wall)
            if cell_value & Direction.WEST.value:
                fill_wall(col_x, col_y + drawing.tile.wall,
                          drawing.tile.wall, drawing.tile.tile)
        col_x = drawing.tile.cols * drawing.tile.passage
        col_y = row_index * drawing.tile.passage
        fill_wall(col_x, col_y, drawing.tile.wall, drawing.tile.wall)
        fill_wall(col_x, col_y + drawing.tile.wall, drawing.tile.wall,
                  drawing.tile.tile)
    col_y = drawing.tile.rows * drawing.tile.passage
    for col_index in range(drawing.tile.cols):
        col_x = col_index * drawing.tile.passage
        fill_wall(col_x, col_y, drawing.tile.wall, drawing.tile.wall)
        fill_wall(col_x + drawing.tile.wall, col_y, drawing.tile.tile,
                  drawing.tile.wall)
    fill_wall(drawing.tile.cols * drawing.tile.passage,
              drawing.tile.rows * drawing.tile.passage, drawing.tile.wall,
              drawing.tile.wall)


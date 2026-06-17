#!/usr/bin/env python3

from visuals.display_classes import DrawInfo, DrawingData
from visuals.drawing_utils import (draw_top_border, draw_left_border,
                                   draw_internal_walls, draw_right_border,
                                   draw_bottom_border, draw_entry, draw_exit)
from mlx import Mlx


def draw_maze(drawing: DrawInfo, mlx: Mlx, mlx_ptr, entry_coord,
              exit_coord) -> None:
    data: DrawingData = DrawingData(drawing, mlx, mlx_ptr)

    draw_top_border(data)
    draw_left_border(data)
    draw_internal_walls(data)
    draw_right_border(data)
    draw_bottom_border(data)
    draw_entry(data, drawing)
    draw_exit(data, drawing)

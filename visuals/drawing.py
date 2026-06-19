#!/usr/bin/env python3

from visuals.display_classes import MazeInfo, DrawingData
from visuals.drawing_utils import (draw_top_border, draw_left_border,
                                   draw_internal_walls, draw_right_border,
                                   draw_bottom_border, draw_entry, draw_exit,
                                   draw_steps)
from mlx import Mlx


def draw_maze(drawing: MazeInfo, mlx: Mlx, mlx_ptr) -> None:
    data: DrawingData = DrawingData(drawing, mlx, mlx_ptr)

    draw_top_border(data)
    draw_left_border(data)
    draw_internal_walls(data)
    draw_right_border(data)
    draw_bottom_border(data)
    draw_entry(data, drawing)
    draw_exit(data, drawing)


def draw_solution(drawing: MazeInfo, mlx, mlx_ptr, entry, exit) -> None:
    data: DrawingData
    step_x: int
    step_y: int

    data = DrawingData(drawing, mlx, mlx_ptr)
    step_x, step_y = entry
    end_x, end_y = exit
    i = 0
    for step in drawing.path:
        if step == "N":
            step_y = step_y - 1
        elif step == "E":
            step_x = step_x + 1
        elif step == "S":
            step_y = step_y + 1
        elif step == "W":
            step_x = step_x - 1
        draw_steps(data, (step_x, step_y))
    # Raise error if last step != exit coord

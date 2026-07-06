#!/usr/bin/env python3

from visuals.display_classes import MazeInfo, DrawingData
from visuals.drawing_utils import (
    draw_top_border,
    draw_left_border,
    draw_internal_walls,
    draw_right_border,
    draw_bottom_border,
    draw_entry,
    draw_exit,
    draw_steps,
    draw_42,
)
from mlx import Mlx
from typing import Any


def draw_maze(drawing: MazeInfo, mlx: Mlx, mlx_ptr: Any) -> None:
    """Orchestrates the drawing of the maze

    Args:
        drawing (MazeInfo): Instance with information for the maze
        mlx (Mlx): Instance containing the Python wrapped mlx
        mlx_ptr (_type_): Pointer to our instance with the graphics server
    """
    data: DrawingData = DrawingData(drawing, mlx, mlx_ptr)

    draw_top_border(data)
    draw_left_border(data)
    draw_internal_walls(data)
    draw_right_border(data)
    draw_bottom_border(data)
    draw_entry(data, drawing)
    draw_exit(data, drawing)
    draw_42(data, drawing)


def draw_solution(
    drawing: MazeInfo,
    mlx: Mlx,
    mlx_ptr: Any,
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> None:
    """Draws the solution path

    Args:
        drawing (MazeInfo): Instance with information for the maze
        mlx (Mlx): Instance containing the Python wrapped mlx
        mlx_ptr (Any): Pointer to our instance with the graphics server
        entry (Tuple): Coordinates to enter the maze
        exit (Tuple): Coordinates to exit the maze
    """
    data: DrawingData
    step_x: int
    step_y: int
    path: str

    path = drawing.path
    data = DrawingData(drawing, mlx, mlx_ptr)
    step_x, step_y = entry
    end_x, end_y = exit
    draw_steps(data, (step_x, step_y), path[0], entry)
    for step_nbr, step in enumerate(path):
        if step == "N":
            step_y = step_y - 1
        elif step == "E":
            step_x = step_x + 1
        elif step == "S":
            step_y = step_y + 1
        elif step == "W":
            step_x = step_x - 1
        if step_nbr + 1 < len(path):
            draw_steps(data, (step_x, step_y), path[step_nbr + 1], entry)

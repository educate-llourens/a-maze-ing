#!/usr/bin/env python3

from visuals.display_errors import DisplayError
from visuals.display_classes import TileInfo, Window, Image, MazeInfo
from visuals.drawing import draw_maze, draw_solution
from mlx import Mlx
from typing import Any


def display_maze(configs: dict) -> None:
    """Extracts the map from the output file of the maze generator, does
    some checks and displays the window for the maze

    Args:
        configs (dict): Dictionary containing the config information

    Raises:
        DisplayError: Any file errors will be raised as a display error
        DisplayError: The width does not match the config width
        DisplayError: The height does not match the config height
        DisplayError: Any error raised during the running window
    """
    maze: list[list[int]] = []
    path: str = ""

    try:
        maze, entry_coord, exit_coord, path = read_hex_map()
    except Exception as msg:
        raise DisplayError(str(msg))
    if len(maze[0]) != configs["WIDTH"]:
        raise DisplayError("Maze width does not equal config width")
    if len(maze) != configs["HEIGHT"]:
        raise DisplayError("Maze height does not equal config height")
    try:
        mlx_display(maze, entry_coord, exit_coord, path)
    except Exception as msg:
        raise DisplayError(str(msg))


def read_hex_map() -> tuple:
    """Reads the output.txt for information to create the map and the path

    Returns:
        int_map: The map filled with ints indicating the wall structure of
        each cell.
        path: The string or directional instructions
    """
    def create_tuple(line: str) -> tuple[int, int]:
        x, y = line.split(",", 1)
        return (int(x), int(y))

    int_map: list[list[int]] = []
    row: list[int] = []
    output_file: str = "tests/output_file.txt"
    # output_file: str = "output_file.txt"
    path: str = ""
    entry: tuple[int, int]
    exit: tuple[int, int]

    with open(output_file, "r") as maze_file:
        for line in maze_file:
            if line == "\n":
                break
            row = [int(char, 16) for char in line.strip()]
            int_map.append(row)
        entry = create_tuple(maze_file.readline().strip())
        exit = create_tuple(maze_file.readline().strip())
        path = maze_file.readline().strip()
    return (int_map, entry, exit, path)


def on_key_press(key_pressed: int, mlx_data: tuple) -> None:
    """When a key is pressed, it will run the process connected to that key.
    Esc (65307) = Exits the program when you press escape
    r   (114)   = Regenerates the maze
    s   (115)   = Shows or hides the solution path
    c   (99)    = Changes the theme of the maze

    Args:
        key_pressed (int): The key that the user pressed
        mlx_data (tuple): A collection of data to regenerate the maze
    """
    mlx: Mlx
    mlx_ptr: Any
    window: Window
    map: list[list[int]]
    entry: tuple
    exit: tuple
    draw_data: MazeInfo

    mlx, mlx_ptr, window, entry, exit, draw_data = mlx_data
    if key_pressed == 114:
        # regenerate maze
        mlx.mlx_clear_window(mlx_ptr, window.ptr)
        map, entry, exit, path = read_hex_map()
        draw_data.maze = map
        draw_data.entry = entry
        draw_data.exit = exit
        draw_data.path = path
        draw_maze(draw_data, mlx, mlx_ptr)
    elif key_pressed == 65307:
        mlx.mlx_loop_exit(mlx_ptr)
    elif key_pressed == 115:  # s
        draw_solution(draw_data, mlx, mlx_ptr, entry, exit)
    elif key_pressed == 99:  # c
        mlx.mlx_clear_window(mlx_ptr, window.ptr)
        if draw_data.alternate is False:
            draw_data.alternate = True
            draw_maze(draw_data, mlx, mlx_ptr)
        else:
            draw_data.alternate = False
            draw_maze(draw_data, mlx, mlx_ptr)


def mlx_display(maze: list[list[int]], entry_coord, exit_coord,
                path: str) -> None:
    """Runs the loop to display and interact the window containing the maze.

    Args:
        maze (list[list[int]]): The maze with its open walls etc as an int
        entry_coord (_type_): The entry coordinates to the maze
        exit_coord (_type_): The exit coordinates to the maze
        path (str): The solution path
    """
    mlx: Mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    tile: TileInfo = TileInfo(maze)
    window: Window = Window(tile, mlx, mlx_ptr)
    image: Image = Image(mlx, mlx_ptr)
    draw_data: MazeInfo = MazeInfo(maze, tile, window, image,
                                   entry_coord, exit_coord, path)

    draw_data.path = path
    draw_maze(draw_data, mlx, mlx_ptr)
    mlx.mlx_hook(window.ptr, 2, 1, on_key_press,
                 ((mlx, mlx_ptr, window, entry_coord, exit_coord, draw_data)))
    mlx.mlx_hook(window.ptr, 33, 0, lambda any: mlx.mlx_loop_exit(mlx_ptr),
                 None)
    mlx.mlx_loop(mlx_ptr)

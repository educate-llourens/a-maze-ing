#!/usr/bin/env python3

from visuals.display_classes import DisplayError
from visuals.display_classes import TileInfo, Window, Image, MazeInfo
from visuals.drawing import draw_maze, draw_solution
from mlx import Mlx
from typing import Any
from mazegen.mazegen import MazeGenerator


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
        mlx_display(maze, entry_coord, exit_coord, path, configs["PERFECT"])
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
    s   (115)   = Shows or hides the solution path
    c   (99)    = Changes the theme of the maze
    i   (105)   = Toggles between imperfect and perfect maze
    d   (100)   = Generates DPS maze (Default maze)
    b   (98)    = Generates BFS maze
    p   (112)   = Generates Prim's maze
    w   (119)   = Generates Wilson maze
    r   (114)   = Generates the same maze

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
    generate_perfect: MazeGenerator
    generate_imperfect: MazeGenerator
    generate_dfs: MazeGenerator
    generate_bfs: MazeGenerator
    generate_prim: MazeGenerator

    mlx, mlx_ptr, window, entry, exit, draw_data = mlx_data
    if key_pressed == 100 or key_pressed == 98 or key_pressed == 112:
        if key_pressed == 100:
            generate_dfs = MazeGenerator(
                draw_data.tile.cols, draw_data.tile.rows,
                draw_data.entry_coord, draw_data.exit_coord, 0,
                draw_data.is_perfect)
            generate_dfs.generate()
            mlx.mlx_loop_exit(mlx_ptr)
            display_maze()
        elif key_pressed == 98:
            generate_bfs = MazeGenerator(
                draw_data.tile.cols, draw_data.tile.rows,
                draw_data.entry_coord, draw_data.exit_coord, 6,
                draw_data.is_perfect)
            generate_bfs.generate()
            mlx.mlx_loop_exit(mlx_ptr)
            display_maze()
        elif key_pressed == 112:
            generate_prim = MazeGenerator(
                draw_data.tile.cols, draw_data.tile.rows,
                draw_data.entry_coord, draw_data.exit_coord, 1,
                draw_data.is_perfect)
            generate_prim.generate()
            mlx.mlx_loop_exit(mlx_ptr)
            display_maze()
    elif key_pressed == 65307:
        mlx.mlx_loop_exit(mlx_ptr)
    elif key_pressed == 114:
        mlx.mlx_clear_window(mlx_ptr, window.ptr)
        draw_maze(draw_data, mlx, mlx_ptr)
    elif key_pressed == 115:
        if draw_data.show_path is False:
            draw_data.show_path = True
            mlx.mlx_clear_window(mlx_ptr, window.ptr)
            draw_maze(draw_data, mlx, mlx_ptr)
            draw_solution(draw_data, mlx, mlx_ptr, entry, exit)
        else:
            draw_data.show_path = False
            mlx.mlx_clear_window(mlx_ptr, window.ptr)
            draw_maze(draw_data, mlx, mlx_ptr)
    elif key_pressed == 99:
        mlx.mlx_clear_window(mlx_ptr, window.ptr)
        if draw_data.alternate is False:
            draw_data.alternate = True
            draw_maze(draw_data, mlx, mlx_ptr)
        else:
            draw_data.alternate = False
            draw_maze(draw_data, mlx, mlx_ptr)
    elif key_pressed == 105:
        if draw_data.is_perfect is True:
            draw_data.is_perfect = False
            generate_imperfect = MazeGenerator(
                draw_data.tile.cols, draw_data.tile.rows,
                draw_data.entry_coord, draw_data.exit_coord, 0, False)
            generate_imperfect.generate()
        else:
            draw_data.is_perfect = True
            generate_perfect = MazeGenerator(
                draw_data.tile.cols, draw_data.tile.rows,
                draw_data.entry_coord, draw_data.exit_coord, 0, True)
            generate_perfect.generate()


def mlx_display(maze: list[list[int]], entry_coord: tuple, exit_coord: tuple,
                path: str, is_perfect: bool) -> None:
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
                                   entry_coord, exit_coord, path, is_perfect)

    draw_data.path = path
    create_info_window(mlx, mlx_ptr)
    draw_maze(draw_data, mlx, mlx_ptr)
    mlx.mlx_hook(window.ptr, 2, 1, on_key_press,
                 ((mlx, mlx_ptr, window, entry_coord, exit_coord, draw_data)))
    mlx.mlx_hook(window.ptr, 33, 0, lambda any: mlx.mlx_loop_exit(mlx_ptr),
                 None)
    mlx.mlx_loop(mlx_ptr)


def create_info_window(mlx: Mlx, mlx_ptr: Any) -> None:
    """Creates a seperate window with instructions on how to interact with
    the maze.

    Args:
        mlx (Mlx): Instance containing the Python wrapped mlx
        mlx_ptr (_type_): Pointer to our instance with the graphics server
    """
    window_ptr = mlx.mlx_new_window(mlx_ptr, 600, 600, "Instructions")
    mlx.mlx_string_put(
        mlx_ptr, window_ptr, 10, 10, 0xFF00FF, "Instructions")
    mlx.mlx_string_put(mlx_ptr, window_ptr, 10, 60, 0xFF00FF,
                       "Press these keys to do the thing:")
    mlx.mlx_string_put(mlx_ptr, window_ptr, 10, 100, 0xFF00FF,
                       "1.  Esc   = Exit the maze and close the window")
    mlx.mlx_string_put(mlx_ptr, window_ptr, 10, 120, 0xFF00FF,
                       "2.  s     = Shows or hides the solution path")
    mlx.mlx_string_put(mlx_ptr, window_ptr, 10, 140, 0xFF00FF,
                       "3.  c     = Changes the theme of the maze")
    mlx.mlx_string_put(mlx_ptr, window_ptr, 10, 160, 0xFF00FF,
                       "4.  r     = Regenerates the same maze")
    mlx.mlx_string_put(mlx_ptr, window_ptr, 10, 180, 0xFF00FF,
                       "5.  d     = Generates DPS maze (Default maze)")
    mlx.mlx_hook(window_ptr, 33, 0, lambda any: mlx.mlx_destroy_window(
        mlx_ptr, window_ptr),
                 None)

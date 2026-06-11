#!/usr/bin/env python3

from visuals.display_errors import DisplayError
from parsing.parsing_errors import FileError
from visuals.display_classes import TileInfo, Window, Image, DrawInfo
from visuals.drawing import draw_maze
from mlx import Mlx


def mlx_display(maze: list[list[int]], entry, exit, path: str) -> None:
    mlx: Mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    tile: TileInfo = TileInfo(maze)
    window: Window = Window(tile, mlx, mlx_ptr)
    image: Image = Image(mlx, mlx_ptr)
    draw_data: DrawInfo = DrawInfo(maze, tile, window, image)

    draw_maze(draw_data, mlx, mlx_ptr)
    mlx.mlx_hook(window.ptr, 33, 0, lambda any: mlx.mlx_loop_exit(mlx_ptr),
                 None)
    mlx.mlx_loop(mlx_ptr)


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


def display_maze(configs: dict) -> None:
    maze: list[list[int]] = []
    path: str = ""

    try:
        maze, entry, exit, path = read_hex_map()
        if len(maze[0]) != configs["WIDTH"]:
            raise DisplayError("Maze width does not equal config width")
        if len(maze) != configs["HEIGHT"]:
            raise DisplayError("Maze height does not equal config height")
    except Exception as msg:
        raise FileError(msg)
    try:
        mlx_display(maze, entry, exit, path)
    except Exception as msg:
        raise DisplayError(msg)

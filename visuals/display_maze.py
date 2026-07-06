#!/usr/bin/env python3

from visuals.display_classes import MapError, MlxError
from parsing.parsing_errors import FileError, ConfigError
from visuals.display_classes import TileInfo, Window, Image, MazeInfo
from visuals.drawing import draw_maze, draw_solution
from mlx import Mlx
from typing import Any, NamedTuple
from mazegen import MazeGenerator, ConfigDict
from mazegen.error import MazeError
from mazegen.cell import Cell


class HexMap(NamedTuple):
    """Store the parsed maze data from a hexadecimal maze file.

    Attributes:
        int_map: Two-dimensional maze represented as hexadecimal wall values.
        entry: Entry cell coordinates.
        exit: Exit cell coordinates.
        path: Shortest solution path as an NSEW string.
    """
    int_map: list[list[int]]
    entry: tuple[int, int]
    exit: tuple[int, int]
    path: str


class HookData(NamedTuple):
    """Store data required by MLX event hooks.

    Attributes:
        mlx: MLX interface instance.
        mlx_ptr: Pointer to the MLX instance.
        window: MLX window instance.
        entry: Entry cell coordinates.
        exit: Exit cell coordinates.
        draw_data: Maze information required for rendering.
        configs: Parsed maze configuration.
    """
    mlx: Mlx
    mlx_ptr: Any
    window: Window
    entry: tuple[int, int]
    exit: tuple[int, int]
    draw_data: MazeInfo
    configs: ConfigDict


def display_maze(configs: ConfigDict, maze_cell: list[list[Cell]]) -> None:
    """Extracts the map from the output file of the maze generator, does
    some checks and displays the window for the maze

    Args:
        configs (dict): Dictionary containing the config information
        maze_cell (list[list[Cell]]):
            grid of cell objects containing each individual cell's information

    Raises:
        DisplayError: Any file errors will be raised as a display error
        DisplayError: The width does not match the config width
        DisplayError: The height does not match the config height
        DisplayError: Any error raised during the running window
    """
    maze_int: list[list[int]] = []
    path: str = ""

    maze_int, entry_coord, exit_coord, path = read_hex_map(configs)
    if len(maze_int[0]) != configs["WIDTH"]:
        raise MapError("Maze width does not equal config width")
    if len(maze_int) != configs["HEIGHT"]:
        raise MapError("Maze height does not equal config height")
    is_perfect: bool = configs["PERFECT"]
    mlx_display(
        maze_int, maze_cell, entry_coord, exit_coord, path, is_perfect, configs
    )


def read_hex_map(configs: ConfigDict) -> HexMap:
    """Reads the output.txt for information to create the map and the path

    Args:
        configs (ConfigDict): configuration dictionary to initialize
        a new maze generator if prompted in a_maze_ing program

    Raises:
        File Error: when reading the output_file from the MazeGenerator
        results in an exception

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
    output_file: str = configs["OUTPUT_FILE"]
    path: str = ""
    entry: tuple[int, int]
    exit: tuple[int, int]

    try:
        with open(output_file, "r") as maze_file:
            for line in maze_file:
                if line == "\n":
                    break
                row = [int(char, 16) for char in line.strip()]
                int_map.append(row)
            entry = create_tuple(maze_file.readline().strip())
            exit = create_tuple(maze_file.readline().strip())
            path = maze_file.readline().strip()
    except Exception as msg:
        raise FileError(str(msg))
    return HexMap(int_map, entry, exit, path)


def on_key_press(key_pressed: int, mlx_data: HookData) -> None:
    """When a key is pressed, it will run the process connected to that key.
    Esc (65307) = Exits the program when you press escape
    s   (115)   = Shows or hides the solution path
    c   (99)    = Changes the theme of the maze
    d   (100)   = Generates DPS maze (Default maze)
    r   (114)   = Redraws the same maze

    Args:
        key_pressed (int): The key that the user pressed
        mlx_data (tuple): A collection of data to regenerate the maze
    """
    mlx: Mlx
    mlx_ptr: Any
    window: Window
    entry: tuple[int, int]
    exit: tuple[int, int]
    draw_data: MazeInfo
    generate_dfs: MazeGenerator
    configs: ConfigDict

    mlx, mlx_ptr, window, entry, exit, draw_data, configs = mlx_data
    if key_pressed == 100:
        try:
            generate_dfs = MazeGenerator(configs)
            generate_dfs.generate()
            generate_dfs.solve()
            generate_dfs.output()
            maze_cell = generate_dfs.grid
        except (ConfigError, MazeError, ValueError, FileError) as msg:
            print(msg)
            return
        new_maze, new_entry, new_exit, new_path = read_hex_map(configs)
        draw_data.maze_int = new_maze
        draw_data.entry_coord = new_entry
        draw_data.exit_coord = new_exit
        draw_data.path = new_path
        draw_data.maze_cell = maze_cell
        mlx.mlx_clear_window(mlx_ptr, window.ptr)
        draw_maze(draw_data, mlx, mlx_ptr)
        if draw_data.show_path is True:
            draw_solution(draw_data, mlx, mlx_ptr, entry, exit)
    elif key_pressed == 65307:
        mlx.mlx_loop_exit(mlx_ptr)
    elif key_pressed == 114:
        mlx.mlx_clear_window(mlx_ptr, window.ptr)
        draw_maze(draw_data, mlx, mlx_ptr)
        if draw_data.show_path is True:
            draw_solution(draw_data, mlx, mlx_ptr, entry, exit)
    elif key_pressed == 115:
        if draw_data.show_path is False:
            draw_data.show_path = True
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
        if draw_data.show_path is True:
            draw_solution(draw_data, mlx, mlx_ptr, entry, exit)


def mlx_display(
    maze_int: list[list[int]],
    maze_cell: list[list[Cell]],
    entry_coord: tuple[int, int],
    exit_coord: tuple[int, int],
    path: str,
    is_perfect: bool,
    configs: ConfigDict,
) -> None:
    """Runs the loop to display and interact the window containing the maze.

    Args:
        maze_int (list[list[int]]): The maze with its open walls etc as an int
        maze_cell (list[list[Cell]]): The maze grid of cells
        entry_coord (_type_): The entry coordinates to the maze
        exit_coord (_type_): The exit coordinates to the maze
        path (str): The solution path
        is_perfect (bool): boolean to say whether or not maze is perfect
        configs (ConfigDict): configuration dictionary

    Raises:
        MlxError: if an mlx window cannot be initialized
        MlxError: if there is an error with the key press hook
        MlxError: if there is an error with the window exit hook
    """
    mlx: Mlx = Mlx()
    try:
        mlx_ptr = mlx.mlx_init()
    except Exception as msg:
        raise MlxError(
            f"mlx could not initialise with error message {str(msg)}"
        )
    tile: TileInfo = TileInfo(maze_int)
    window: Window = Window(tile, mlx, mlx_ptr)
    image: Image = Image(mlx, mlx_ptr)
    draw_data: MazeInfo = MazeInfo(
        maze_int,
        maze_cell,
        tile,
        window,
        image,
        entry_coord,
        exit_coord,
        path,
        is_perfect,
    )

    draw_data.path = path
    try:
        create_info_window(mlx, mlx_ptr)
    except Exception as msg:
        raise MlxError(
            f"Could not create info window with error message {str(msg)}"
        )
    draw_maze(draw_data, mlx, mlx_ptr)
    try:
        mlx.mlx_hook(
            window.ptr,
            2,
            1,
            on_key_press,
            HookData(
                mlx,
                mlx_ptr,
                window,
                entry_coord,
                exit_coord,
                draw_data,
                configs,
            ),
        )
    except Exception as msg:
        raise MlxError(f"Issue with key press hook with error message {msg}")
    try:
        mlx.mlx_hook(
            window.ptr, 33, 0, lambda any: mlx.mlx_loop_exit(mlx_ptr), None
        )
    except Exception as msg:
        raise MlxError(
            f"Issue with window exit hook with error message {str(msg)}"
        )
    mlx.mlx_loop(mlx_ptr)


def create_info_window(mlx: Mlx, mlx_ptr: Any) -> None:
    """Creates a seperate window with instructions on how to interact with
    the maze.

    Args:
        mlx (Mlx): Instance containing the Python wrapped mlx
        mlx_ptr (_type_): Pointer to our instance with the graphics server
    """
    window_ptr = mlx.mlx_new_window(mlx_ptr, 600, 600, "Instructions")
    mlx.mlx_string_put(mlx_ptr, window_ptr, 10, 10, 0xFF00FF, "Instructions")
    mlx.mlx_string_put(
        mlx_ptr,
        window_ptr,
        10,
        60,
        0xFF00FF,
        "Press these keys to do the thing:",
    )
    mlx.mlx_string_put(
        mlx_ptr,
        window_ptr,
        10,
        100,
        0xFF00FF,
        "1.  Esc   = Exit the maze and close the window",
    )
    mlx.mlx_string_put(
        mlx_ptr,
        window_ptr,
        10,
        120,
        0xFF00FF,
        "2.  s     = Shows or hides the solution path",
    )
    mlx.mlx_string_put(
        mlx_ptr,
        window_ptr,
        10,
        140,
        0xFF00FF,
        "3.  c     = Changes the theme of the maze",
    )
    mlx.mlx_string_put(
        mlx_ptr,
        window_ptr,
        10,
        160,
        0xFF00FF,
        "4.  r     = Regenerates the same maze",
    )
    mlx.mlx_string_put(
        mlx_ptr,
        window_ptr,
        10,
        180,
        0xFF00FF,
        "5.  d     = Generates DPS maze (Default maze)",
    )
    mlx.mlx_hook(
        window_ptr,
        33,
        0,
        lambda any: mlx.mlx_destroy_window(mlx_ptr, window_ptr),
        None,
    )

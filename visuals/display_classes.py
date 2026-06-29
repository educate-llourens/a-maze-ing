from enum import Enum
from mlx import Mlx
from typing import Any

# Classes in file -------------------------------------------------------------
# 1.  DisplayError
# 2.  TileInfo
# 3.  Window
# 4.  Image
# 5.  MazeInfo
# 6.  DrawingData
# 7.  Direction
# -----------------------------------------------------------------------------


class DisplayError(Exception):
    """Shows errors that are specifically around the visuals of the maze.

    Args:
        Exception (_type_)
    """
    def __init__(self, msg):
        """Shows errors related to displaying the maze.

        Args:
            msg (str): The message to display if an error happens
        """
        known_error_str = ["Map Error:", "Mlx Error:", "Drawing Error:"]
        for item in known_error_str:
            if item in msg:
                super().__init__(msg)
                break
            else:
                super().__init__(f"Display Error: {msg}")


class MapError(DisplayError):
    """Shows errors related to the map

    Args:
        DisplayError (Exception):
    """
    def __init__(self, msg: str):
        """Creates a map error

        Args:
            msg (str): Message to display if the error happenss
        """
        super().__init__(f"Map Error: {msg}")


class MlxError(DisplayError):
    """Shows errors related to an mlx issue

    Args:
        DisplayError (Exception):
    """
    def __init__(self, msg: str):
        """Creates a Mlx error

        Args:
            msg (str): Message to display if the error happens
        """
        super().__init__(f"Mlx Error: {msg}")


class DrawingError(DisplayError):
    def __init__(self, msg: str):
        super().__init__(f"Drawing Error: {msg}")


class TileInfo:
    """Contains the information for the tile or cell
    """
    def __init__(self, maze: list[list[int]]) -> None:
        """Creates an instance of TileInfo with the necessary information to
        draw the cell.

        Args:
            maze (list[list[int]]): The maze map as a grid of ints. Each int
            contains information for which walls are open or closed.
        """
        self.image_size = 32
        self.tile: int = self.image_size
        self.wall: int = self.image_size
        self.passage: int = self.tile + self.wall
        self.rows: int = len(maze)
        self.cols: int = len(maze[0])


class Window:
    """Contains imprtant information for displaying a window
    """
    def __init__(self, tile: TileInfo, mlx: Mlx, mlx_ptr: Any):
        """Creates an instance of a window with important information to
        display it.

        Args:
            tile (TileInfo): Information for the tile / cell to display
            mlx (Mlx): Instance containing the Python wrapped mlx
            mlx_ptr (_type_): Pointer to our instance with the graphics server
        """
        self.width = tile.cols * tile.passage + tile.wall
        self.height = tile.rows * tile.passage + tile.wall
        self.ptr = mlx.mlx_new_window(mlx_ptr, self.width, self.height,
                                      "A-maze-ing")


class Image:
    """Contains all the information for the images to display
    """
    def __init__(self, mlx: Mlx, mlx_ptr: Any) -> None:
        """Creates an Image instance for all the images that ca be used

        Args:
            mlx (Mlx): The mlx instance we are using
            mlx_ptr (_type_): Pointer to our instance with the graphics server
        """
        walls = mlx.mlx_png_file_to_image(mlx_ptr,
                                          "./visuals/assets/wall.png")
        self.wall_ptr, self.wall_width, self.wall_height = walls
        if not self.wall_ptr:
            print("Failed to load wall image!")
        start = mlx.mlx_png_file_to_image(mlx_ptr,
                                          "./visuals/assets/start.png")
        self.start_ptr, self.start_width, self.start_height = start
        if not self.start_ptr:
            print("Failed to load start image!")
        end = mlx.mlx_png_file_to_image(mlx_ptr,
                                        "./visuals/assets/end.png")
        self.end_ptr, self.end_width, self.end_height = end
        if not self.end_ptr:
            print("Failed to load end image!")
        alt_walls = mlx.mlx_png_file_to_image(
            mlx_ptr, "./visuals/assets/alt_wall.png")
        self.alt_wall_ptr, self.alt_walls_width, self.alt_walls_height = (
            alt_walls)
        alt_start = mlx.mlx_png_file_to_image(
            mlx_ptr, "./visuals/assets/alt_start.png")
        self.alt_start_ptr, self.alt_start_width, self.alt_start_height = (
            alt_start)
        alt_end = mlx.mlx_png_file_to_image(
            mlx_ptr, "./visuals/assets/alt_end.png")
        self.alt_end_ptr, self.alt_end_width, self.alt_end_height = (
            alt_end)
        steps = mlx.mlx_png_file_to_image(mlx_ptr, "./visuals/assets/steps.png")
        self.steps_ptr, self.steps_width, self.steps_height = steps


class MazeInfo:
    """Contains information and instances to help create a display for
    the maze
    """
    def __init__(self, maze: list[list[int]], tile: TileInfo, window: Window,
                 image: Image, entry_coord: tuple, exit_coord: tuple,
                 path: str, is_perfect: bool) -> None:
        """Creates an instance of MazeInfo containing important information
        and instances to create a display for the maze

        Args:
            maze (list[list[int]]): The maze map as a grid of ints.
            tile (TileInfo): Instance with informatio of the tile / cell
            window (Window): Instance with information for displaying
            the window
            image (Image): Instance with information for displaying the
            png images
            entry_coord (tuple): Coordinate to enter the maze
            exit_coord (tuple): Coordinate to exit the maze
            path (str): String containing the solution path
        """
        self.maze = maze
        self.tile = tile
        self.window = window
        self.image = image
        self.entry_coord = entry_coord
        self.exit_coord = exit_coord
        self.path = path
        self.alternate = False
        self.show_path = False
        self.is_perfect = is_perfect


class DrawingData:
    """Contains information for drawing the maze and its solution path
    """
    def __init__(self, drawing: MazeInfo, mlx: Mlx, mlx_ptr: Any) -> None:
        """Creates an instance of DrawingData containg all the information
        for drawing the maze and its features.

        Args:
            drawing (MazeInfo): Maze information instance for drawing the maze
            mlx (Mlx): Instance containing the Python wrapped mlx
            mlx_ptr (Any): Pointer to our instance with the graphics server
        """
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
        self.alternate = drawing.alternate
        self.show_path = drawing.show_path
        self.path = drawing.path


class Direction(Enum):
    """Puts the directions in a nice ENUM to help make the directions easier

    Args:
        Enum (_type_):
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

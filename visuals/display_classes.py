from enum import Enum
from mlx import Mlx


class TileInfo:
    def __init__(self, maze: list[list[int]]):
        self.image_size = 48
        self.tile: int = self.image_size
        self.wall: int = self.image_size
        self.passage: int = self.tile + self.wall
        self.rows: int = len(maze)
        self.cols: int = len(maze[0])


class Window:
    def __init__(self, tile: TileInfo, mlx: Mlx, mlx_ptr):
        self.width = tile.cols * tile.passage + tile.wall
        self.height = tile.rows * tile.passage + tile.wall
        self.ptr = mlx.mlx_new_window(mlx_ptr, self.width, self.height,
                                      "A-maze-ing")


class Image:
    def __init__(self, mlx: Mlx, mlx_ptr):
        self.ptr, self.width, self.height = mlx.mlx_png_file_to_image(
            mlx_ptr, "./visuals/assets/brick_wall.png")


class DrawInfo:
    def __init__(self, maze: list[list[int]], tile: TileInfo, window: Window,
                 image: Image):
        self.maze = maze
        self.tile = tile
        self.window = window
        self.image = image


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

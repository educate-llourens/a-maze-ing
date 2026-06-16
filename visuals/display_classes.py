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
        walls = mlx.mlx_png_file_to_image(mlx_ptr,
                                          "./visuals/assets/wall.png")
        self.wall_ptr, self.wall_width, self.wall_height = walls
        start = mlx.mlx_png_file_to_image(mlx_ptr,
                                          "./visuals/assets/start.png")
        self.start_ptr, self.start_width, self.start_height = start
        end = mlx.mlx_png_file_to_image(mlx_ptr,
                                        "./visuals/assets/end.png")
        self.end_ptr, self.end_width, self.end_height = end


class DrawInfo:
    def __init__(self, maze: list[list[int]], tile: TileInfo, window: Window,
                 image: Image, entry_coord, exit_coord):
        self.maze = maze
        self.tile = tile
        self.window = window
        self.image = image
        self.entry_coord = entry_coord
        self.exit_coord = exit_coord


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

#!/usr/bin/env python3

from typing import List
from random import randint
from cell import Cell

class   MazeGenerator:
    """ 
    MazeGenerator is a class that can be imported via the mazegen module.
    It is used to generate a maze and its shortest path solution.

    To create an instance of the class (and thus then use the generate() method)
    it is essential to pass the specified parameters for the maze.

    Width: int = Maze width (number of cells)
    Height: int = Maze height
    Start: tuple[int, int] =  Entry coordinates (x, y)
    End: tuple[int, int] = Exit coordinates (x, y)
    Perfect: boolean = True for a perfect maze, False for imperfect maze
    Seed (OPTIONAL): str = any string
    Algorithm (OPTIONAL): int = 
    0 (DEFAULT) Depth-First Search (Recursive Backtracking)
    1 Prim's Algorithm
    2 Wilson's Algorithm

    The generate() method will generate a maze given the specified parameters,
    and also give the shortest path (solution) with this generated maze.
    Both the maze, entry and exit and path will be provided in an output file.
    This output file can be found in the root directory of the program,
    namely "output_maze.txt".
    """

    def __init__(self, width: int, height: int, start: tuple[int, int],
                 end: tuple[int, int], algorithm: int = 0,
                 perfect: bool = True, seed: str | None = None) -> None:
            self.width = width
            self.height = height
            self.start = start
            self.end = end
            self.perfect = perfect
            self.seed = seed
            self.algorithm = algorithm
            self.maze = [[Cell(x, y) for x in range(width)] for y in range(height)]


    def test(self):
        self._42()
        maze_string = self._maze_to_str()
        path = "haha"
        self._output(maze_string, path)


    def generate(self) -> None:
        self._42()
        if self.algorithm == 0:
            self._dfs()
            if self.perfect is False:
                self._imperfect(maze)
        elif self.algorithm == 1:
            self._prim()
        elif self.algorithm == 2:
            self._wilson()
        maze_string = self._maze_to_str()
        path = "haha"
        self._output(maze_string, path)

    def _42(self):
        """ Function that will block 4 and 2 pattern in maze grid """
        if self.width < 11 or self.height < 9:
            raise SizeError("Size of maze too small for 42 pattern!")
            return
        mid_x = int(self.width / 2)
        mid_y = int(self.height / 2)
        offset_4 = -1
        offset_2 = 1
        if self.width % 2 == 0:
            offset_4 = -2
            offset_2 = 1
        cells_4 = [
                (mid_x - 2, mid_y - 2), (mid_x - 2, mid_y - 1), (mid_x - 2, mid_y),
                (mid_x - 1, mid_y), (mid_x, mid_y), (mid_x, mid_y + 1),
                (mid_x, mid_y + 2) 
        ]
        cells_2 = [
            (mid_x + 2, mid_y - 2), (mid_x + 2, mid_y - 1), (mid_x + 2, mid_y),
            (mid_x + 2, mid_y + 2),
            (mid_x + 1, mid_y + 2), (mid_x + 1, mid_y - 2), (mid_x + 1, mid_y),
            (mid_x, mid_y - 2), (mid_x, mid_y), (mid_x, mid_y + 1),
            (mid_x, mid_y + 2)
        ]
        for x, y in cells_4:
            self.maze[y][x + offset_4].blocked = True
        for x, y in cells_2:
            self.maze[y][x + offset_2].blocked = True


    def _get_cell(self, x: int, y: int) -> "Cell":
        """ Returns cell object at specified coordinate of maze nested list"""
        if x < 0 or x > self.width - 1:
            return None
        if y < 0 or y > self.height - 1:
            return None
        return (self.maze[y][x])


    def _get_neighbors(self, node: "Cell") -> list["Cell"]:
        node_neighbors = []
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x, y in neighbors:
            neighbor = self._get_cell((node.x + x), (node.y + y))
            if neighbor is not None:
                node_neighbors.append(self._get_cell((node.x + x), (node.y + y)))
        return node_neighbors

    def _is_unvisited(self, node: "Cell") -> bool:
        if node.visited == True or node.blocked == True:
            return False
        return True


    def _get_unvisited_neighbors(self, neighbors: list["Cell"]) -> list["Cell"]:
        unvisited = []
        for neighbor in neighbors:
            if self._is_unvisited(neighbor):
                unvisited.append(neighbor)
        return unvisited


    def _dfs(self) -> None:
        start = self._get_cell(self.start[0], self.start[1])
        stack = [start]

        while len(stack) != 0:
            current = stack.pop()
            neighbors = self._get_neighbors(current)
            unvisited = self._get_unvisited_neighbors(neighbors)
            if len(unvisited) != 0:
                stack.append(current)
                index = randint(0, len(unvisited) - 1)
                chosen = unvisited[index]
                self._remove_walls(current, chosen)
                chosen.visited = True
                stack.append(chosen)


    def _remove_walls(self, current: "Cell", chosen: "Cell") -> None:
        if current.x < chosen.x:
            current.walls = self._open_wall(1, current.walls)
            chosen.walls = self._open_wall(3, chosen.walls)
        if current.x > chosen.x:
            current.walls = self._open_wall(3, current.walls)
            chosen.walls = self._open_wall(1, chosen.walls)
        if current.y < chosen.y:
            current.walls = self._open_wall(0, current.walls)
            chosen.walls = self._open_wall(2, chosen.walls)
        if current.y > chosen.y:
            current.walls = self._open_wall(2, current.walls)
            chosen.walls = self._open_wall(0, chosen.walls)    


    def _prim(self) -> None:
        return


    def _wilson(self) -> None:
        return
    

    def _output(self, maze: str, path: str) -> None:
        try:
            with open("output_maze.txt", "w") as output:
                output.write(maze)
                output.write("\n")
                output.write(f"{self.start[0]},{self.start[1]}\n")
                output.write(f"{self.end[0]},{self.end[1]}\n")
                output.write(path + "\n")
        except Exception as e: # maybe our personal generation error?
            print(f"Output file generation error: {e}")


# dict with collection of cells, their position (x,y), their 

    def _open_wall(self, dir: int, cell: hex) -> hex:
        if dir == 0: # north (up)
            return (cell & ~0x1)
        if dir == 1: # east (right)
            return (cell & ~0x2)
        if dir == 2: # south (down)
            return (cell & ~0x4)
        if dir == 3: # west (left)
            return (cell & ~0x8)

#not sure where this would be useful but hey
        def _close_wall(dir: int, cell: hex) -> hex:
            if dir == 0: # north (up)
                return (cell | (1<<0))
            if dir == 1: # east (right)
                return (cell | (1<<1))
            if dir == 2: # south (down)
                return (cell | (1<<2))
            if dir == 3: # west (left)
                return (cell | (1<<3))

    
    def _maze_to_str(self):
        string = ""
        for y in range(0, self.height):
            for x in range(0, self.width):
                result = "%X" % self.maze[y][x].walls
                string += result
                x += 1
            string += "\n"
            y += 1
        return string
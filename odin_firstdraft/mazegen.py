#!/usr/bin/env python3

from typing import List
import random
from cell import Cell


class MazeGenerator:
    """"""

    # init / grid setup
    def __init__(self, width: int, height: int, start: tuple[int, int],
                 end: tuple[int, int], algorithm: int = 0,
                 perfect: bool = True, seed: int | None = None) -> None:
        self._width = width
        self._height = height
        self._start = start
        self._end = end
        self._perfect = perfect
        self._seed = seed
        self._algorithm = algorithm
        self._maze = [
                [Cell(x, y) for x in range(width)]
                for y in range(height)
                ]
        if seed is not None:
            random.seed(self._seed)
        self._path = ""

    def generate(self) -> None:
        """ Public method called to generate the maze.
        The generated maze is stored in the self._maze property """
        self._42()
        if self._algorithm == 0:
            self._dfs()
            if self._perfect is False:
                self._imperfect()

    # generation internals
    def _42(self) -> None:
        """ Method to block off the 4 and 2 in the middle of the maze,
        if there is enough space given the weight/height parameters. """
        if self._width < 11 or self._height < 9:
            print("Size of maze too small for 42 pattern!")
        else:
            mid_x = int(self._width / 2)
            mid_y = int(self._height / 2)
            offset_4 = -1
            offset_2 = 1
            if self._width % 2 == 0:
                offset_4 = -2
                offset_2 = 1
            cells_4 = [
                    (mid_x - 2, mid_y - 2), (mid_x - 2, mid_y - 1),
                    (mid_x - 2, mid_y), (mid_x - 1, mid_y), (mid_x, mid_y),
                    (mid_x, mid_y + 1), (mid_x, mid_y + 2)
            ]
            cells_2 = [
                (mid_x + 2, mid_y - 2), (mid_x + 2, mid_y - 1),
                (mid_x + 2, mid_y), (mid_x + 2, mid_y + 2),
                (mid_x + 1, mid_y + 2), (mid_x + 1, mid_y - 2),
                (mid_x + 1, mid_y), (mid_x, mid_y - 2), (mid_x, mid_y),
                (mid_x, mid_y + 1), (mid_x, mid_y + 2)
            ]
            for x, y in cells_4:
                self._maze[y][x + offset_4].four = True
            for x, y in cells_2:
                self._maze[y][x + offset_2].two = True

    def _imperfect(self) -> None:
        """ Method called when DFS algorithm is used,
        and the maze generation has to lead to an imperfect maze.
        Imperfect maze is achieved by removing roughly 10 perfect of
        all internal walls after dfs maze generation"""
        internal_walls = self._count_walls()
        amount_to_remove = int(0.1 * internal_walls)
        while amount_to_remove > 0:
            x = random.randint(0, self._width - 1)
            y = random.randint(0, self._height - 1)
            bit = random.randint(0, 3)
            if y == 0 and bit == 0:  # north wall cannot open
                while y == 0:
                    y = random.randint(0, self._height - 1)
            if y == self._height - 1 & bit == 2:  # south wall cannot open
                while y == self._height - 1:
                    x = random.randint(0, self._height - 1)
            if x == 0 and bit == 3:  # west wall cannot open
                while x == 0:
                    x = random.randint(0, self._width - 1)
            if x == self._width - 1 and bit == 1:  # east wall cannot open
                while x == self._width - 1:
                    x = random.randint(0, self._width - 1)
            if self._allowed_removal(x, y, bit):
                cell = self._get_cell(x, y)
                direction = self._get_direction(bit)
                neighbor = self._get_cell(x + direction[0], y + direction[1])
                self._remove_walls(cell, neighbor)
                amount_to_remove -= 1

    def _dfs(self) -> None:
        """ Method called to generate the maze using depth-first search.
        DFS will create a perfect maze, and adjust the bits of the .walls
        property in the objects of class Cell """
        start = self._get_cell(self._start[0], self._start[1])
        stack = [start]
        while len(stack) != 0:
            current = stack.pop()
            neighbors = self._get_neighbors(current)
            unvisited = self._get_unvisited_neighbors(neighbors)
            if len(unvisited) != 0:
                stack.append(current)
                index = random.randint(0, len(unvisited) - 1)
                chosen = unvisited[index]
                self._remove_walls(current, chosen)
                chosen.visited = True
                stack.append(chosen)

    # generation helpers
    def _is_unvisited(self, node: "Cell") -> bool:
        """ Returns True if node is unvisited (or allowed to be visited),
        returns False if node is visited (or not allowed to be visited)"""
        if node.visited is True or node.four is True or node.two is True:
            return False
        return True

    def _get_unvisited_neighbors(self,
                                 neighbors: list["Cell"]) -> list["Cell"]:
        """ Takes a list of cell objects and sees which ones are unvisited """
        unvisited = []
        for neighbor in neighbors:
            if self._is_unvisited(neighbor):
                unvisited.append(neighbor)
        return unvisited

    def _count_walls(self) -> int:
        """ Counts the amount of internal walls in the maze grid """
        count = 0
        for y in range(self._height):
            for x in range(self._width):
                cell = self._get_cell(x, y)
                if x < self._width - 1:
                    if cell.walls >> 1 & 1:
                        count += 1
                if y < self._height - 1:
                    if cell.walls >> 2 & 1:
                        count += 1
        return count

    def _allowed_removal(self, x: int, y: int, bit: int) -> bool:
        """ Returns True if removal does not violate the constraints of
        an imperfect maze (no 3x3 open space, 42 in the middle), returns
        False if removal is not allowed / would violate these constraints """
        cell = self._get_cell(x, y)
        direction = self._get_direction(bit)
        neighbor = self._get_cell(x + direction[0], y + direction[1])
        if neighbor is None:
            return False
        if cell.four or cell.two or neighbor.four or neighbor.two:
            return False
        if cell.walls >> bit & 1:
            if not self._3x3:
                self._add_walls(cell, neighbor)
                return True
        return False

    def _3x3(self, x: int, y: int, bit: int) -> bool:
        """ Checks whether the removal of an internal wall creates
        a 3x3 open space. Returns False if it does not, returns True
        if it does. """
        cell = self._get_cell(x, y)
        direction = self._get_direction(bit)
        neighbor = self._get_cell(x + direction[0], y + direction[1])
        self._remove_walls(cell, neighbor)
        if cell.walls != hex(0):
            return False
        neighbors = self._get_neighbors(cell)
        for n in neighbors:
            neighbit = self._get_bit(neighbor.x - x, neighbor.y - y)
            if n.walls is not hex(neighbit):
                return False
        self._add_walls(cell, neighbor)
        return True

    # solving
    def solve(self) -> None:
        """ Public method: solves the generated maze grid by using self._bfs()
        and exports the path it found by updating the string self._path """
        path = self._bfs()
        self._cell_path_to_str(path)

    def _bfs(self) -> list["Cell"] | None:
        """ Method that solves the generated maze grid by using basic
        breadth-first search. Returns a list of nodes (the shortest path).
        Start cell is at index -1, end cell is at 0, so from end to start """
        start = self._get_cell(self._start[0], self._start[1])
        end = self._get_cell(self._end[0], self._end[1])
        visited = []
        queue = []
        came_from = {}
        
        queue.append(start)
        visited.append(start)
        current = start

        while queue and current is not end:
            current = queue.pop(0)
            neighbors = self._get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited and self._allowed_entry(
                        current, neighbor):
                    came_from[neighbor] = current
                    queue.append(neighbor)
                    visited.append(neighbor)

        if current is not end:
            print("End was not found")
            return None
        else:
            path = self._return_path(came_from, start, end)
            return path

    # solving helpers

    def _return_path(self, came_from: dict["Cell", "Cell"],
                     start: "Cell", end: "Cell") -> list["Cell"]:
        """ Takes a dictionary where key:value is to be read as:
            'key node comes from value node', used to backtrack
            the path found by the bfs method """
        path = []
        current = end
        while current is not start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        return path

    def _allowed_entry(self, current: "Cell", neighbor: "Cell") -> bool:
        """ Returns True if the wall between current and neighbor is open,
        returns False if it is closed. Used by bfs algorithm to check
        whether this neighbor is an available option to go to """
        bit = self._get_bit(current.x - neighbor.x, current.y - neighbor.y)
        if neighbor.walls >> bit & 1:
            return False
        return True

    def _cell_path_to_str(self, path: list["Cell"]) -> None:
        """ Takes a list of nodes, the path found by the bfs algorithm,
        then reads this node by node (from the end as that is the start node),
        and translates this into a string, path, with NESW directions """
        current = None
        end = path[0]
        while current is not end:
            current = path.pop(-1)
            if current is end:
                break
            following = path[-1]
            direction = self._coord_to_direction(
                    current.x, following.x, current.y, following.y
                    )
            self._path += direction

    # public access
    @property
    def grid(self) -> List[list["Cell"]]:
        """ Returns the maze grid, list of list of cell objects """
        return self._maze

    @property
    def solution(self) -> str:
        """ Returns the path / solution string """
        return self._path

    # mazegen utilities
    def _get_cell(self, x: int, y: int) -> None | "Cell":
        """ Returns the cell object at (x, y) in the maze grid """
        if x < 0 or x > self._width - 1:
            return None
        if y < 0 or y > self._height - 1:
            return None
        return (self._maze[y][x])

    def _get_neighbors(self, node: "Cell") -> list["Cell"]:
        """ Returns all neighbors of a cell object in the maze grid """
        node_neighbors = []
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x, y in neighbors:
            neighbor = self._get_cell((node.x + x), (node.y + y))
            if neighbor is not None:
                node_neighbors.append(
                        self._get_cell((node.x + x), (node.y + y))
                        )
        return node_neighbors

    def _remove_walls(self, current: "Cell", chosen: "Cell") -> None:
        """ Removes the wall between the current and chosen node,
        from both sides to ensure an open passage """
        if current.x < chosen.x:
            current.walls = self._open_wall(1, current.walls)
            chosen.walls = self._open_wall(3, chosen.walls)
        if current.x > chosen.x:
            current.walls = self._open_wall(3, current.walls)
            chosen.walls = self._open_wall(1, chosen.walls)
        if current.y > chosen.y:
            current.walls = self._open_wall(0, current.walls)
            chosen.walls = self._open_wall(2, chosen.walls)
        if current.y < chosen.y:
            current.walls = self._open_wall(2, current.walls)
            chosen.walls = self._open_wall(0, chosen.walls)

    def _add_walls(self, current: "Cell", chosen: "Cell") -> None:
        """ Adds walls between the current and chosen node,
        from both sides to ensure a closed passage """
        if current.x < chosen.x:
            current.walls = self._close_wall(1, current.walls)
            chosen.walls = self._close_wall(3, chosen.walls)
        if current.x > chosen.x:
            current.walls = self._close_wall(3, current.walls)
            chosen.walls = self._close_wall(1, chosen.walls)
        if current.y > chosen.y:
            current.walls = self._close_wall(0, current.walls)
            chosen.walls = self._close_wall(2, chosen.walls)
        if current.y < chosen.y:
            current.walls = self._close_wall(2, current.walls)
            chosen.walls = self._close_wall(0, chosen.walls)

    def _open_wall(self, dir: int, cell: hex) -> hex:
        """ Returns the hexadecimal value after opening a wall,
        changing that bit from 1 -> 0, given a hexadecimal value,
        and the direction (bit 0-3) that needs to be opened """
        if dir == 0:  # north (up)
            return (cell & ~0x1)
        if dir == 1:  # east (right)
            return (cell & ~0x2)
        if dir == 2:  # south (down)
            return (cell & ~0x4)
        if dir == 3:  # west (left)
            return (cell & ~0x8)

    def _close_wall(self, dir: int, cell: hex) -> hex:
        """ Returns the hexadecimal value after closing a wall,
        changing that bit from 0 -> 1, given a hexadecimal value,
        and the direction (bit 0-3) that needs to be closed """
        if dir == 0:  # north (up)
            return (cell | (1 << 0))
        if dir == 1:  # east (right)
            return (cell | (1 << 1))
        if dir == 2:  # south (down)
            return (cell | (1 << 2))
        if dir == 3:  # west (left)
            return (cell | (1 << 3))

    # bit utilities
    @staticmethod
    def _get_direction(bit: int) -> tuple[int, int]:
        """ Returns the direction coordinates given a specific bit """
        if bit == 0:
            return (0, -1)
        elif bit == 1:
            return (1, 0)
        elif bit == 2:
            return (0, 1)
        elif bit == 3:
            return (-1, 0)
        return (0, 0)

    @staticmethod
    def _get_bit(x: int, y: int) -> int:
        """ Returns a bit given the specific direction coordinates """
        if y == -1:
            return 0
        if x == 1:
            return 1
        if y == 1:
            return 2
        if x == -1:
            return 3
        return -1

    @staticmethod
    def _coord_to_direction(x1: int, x2: int, y1: int, y2: int) -> str:
        """ Returns NSEW direction given specific direction coordinates """
        if x1 > x2:
            return 'W'
        if x1 < x2:
            return 'E'
        if y1 > y2:
            return 'N'
        if y1 < y2:
            return 'S'

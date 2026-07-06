#!/usr/bin/env python3

from typing import List, TypedDict
import random
from .cell import Cell
from .error import MazeError
from parsing.parsing_errors import FileError


class ConfigDict(TypedDict):
    """Configuration required to generate a maze.

    Attributes:
        WIDTH: Maze width in cells.
        HEIGHT: Maze height in cells.
        ENTRY: Entry coordinates.
        EXIT: Exit coordinates.
        OUTPUT_FILE: Output filename.
        PERFECT: Whether to generate a perfect maze.
        SEED: Optional random seed.
    """
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int | None


class MazeGenerator:
    """Generate, solve, and export mazes based on a configuration."""

    # init / grid setup
    def __init__(self, config: ConfigDict) -> None:
        """Initialize a maze generator from a configuration.

        Creates the maze grid, stores the generation parameters, and
        validates that the entry and exit do not lie inside the 42 pattern.

        Args:
            config: Dictionary containing the maze configuration. It must
                define the width, height, entry and exit coordinates,
                output filename, whether the maze should be perfect,
                and an optional random seed.

        Raises:
            MazeError: If the entry or exit coordinates lie inside the
                generated 42 pattern.
        """
        self._width: int = config["WIDTH"]
        self._height: int = config["HEIGHT"]
        self._start: tuple[int, int] = config["ENTRY"]
        self._end: tuple[int, int] = config["EXIT"]
        self._perfect: bool = config["PERFECT"]
        self._seed: int | None = config["SEED"]
        self._maze: List[list[Cell]] = [
            [Cell(x, y) for x in range(self._width)]
            for y in range(self._height)
        ]
        self._path: str = ""
        self._structure: str = ""
        self._file_name: str = config["OUTPUT_FILE"]
        if self._in_42():
            raise MazeError("Start and end must not be in 42 pattern.")

    def generate(self) -> None:
        """Generate the maze.

        Creates the optional 42 pattern, generates the maze using
        depth-first search, optionally makes it imperfect, and stores
        the hexadecimal maze representation.
        """
        if self._seed is not None:
            random.seed(self._seed)
        try:
            self._42()
        except MazeError as e:
            print(f"{e}: continue generating without 42 pattern.")
        self._dfs()
        if self._perfect is False:
            self._imperfect()
        self._structure = self._maze_to_str()

    # generation internals
    def _42(self) -> None:
        """Mark the cells that form the 42 pattern.

        Raises:
            MazeError: If the maze is too small to contain the pattern.
        """
        if self._width < 11 or self._height < 9:
            raise MazeError("Size of maze too small for 42 pattern")
        mid_x = int(self._width / 2)
        mid_y = int(self._height / 2)
        offset_4 = -1
        offset_2 = 1
        if self._width % 2 == 0:
            offset_4 = -2
            offset_2 = 1
        cells_4 = [
            (mid_x - 2, mid_y - 2),
            (mid_x - 2, mid_y - 1),
            (mid_x - 2, mid_y),
            (mid_x - 1, mid_y),
            (mid_x, mid_y),
            (mid_x, mid_y + 1),
            (mid_x, mid_y + 2),
        ]
        cells_2 = [
            (mid_x + 2, mid_y - 2),
            (mid_x + 2, mid_y - 1),
            (mid_x + 2, mid_y),
            (mid_x + 2, mid_y + 2),
            (mid_x + 1, mid_y + 2),
            (mid_x + 1, mid_y - 2),
            (mid_x + 1, mid_y),
            (mid_x, mid_y - 2),
            (mid_x, mid_y),
            (mid_x, mid_y + 1),
            (mid_x, mid_y + 2),
        ]
        for x, y in cells_4:
            self._maze[y][x + offset_4].four = True
        for x, y in cells_2:
            self._maze[y][x + offset_2].two = True

    def _in_42(self) -> bool:
        """Check whether the entry or exit lies inside the 42 pattern.

        Raises:
            MazeError: if the configured cell is not defined.

        Returns:
            True if either coordinate belongs to the 42 pattern,
            otherwise False.
        """
        check = [self._start, self._end]
        try:
            self._42()
        except MazeError:
            return False
        for y in range(0, self._height):
            for x in range(0, self._width):
                cell = self._get_cell(x, y)
                if cell is None:
                    raise MazeError("Cell not defined")
                if cell.four or cell.two:
                    if check[0][0] == cell.x and check[0][1] == cell.y:
                        return True
                    if check[1][0] == cell.x and check[1][1] == cell.y:
                        return True
        return False

    def _imperfect(self) -> None:
        """Convert the generated perfect maze into an imperfect maze.

        Removes a percentage of internal walls while preserving the
        project constraints.

        Raises:
            MazeError: If a configured cell or neighbor is not defined.
        """
        internal_walls = self._count_walls()
        amount_to_remove = int(0.2 * internal_walls)
        while amount_to_remove > 0:
            x = random.randint(0, self._width - 1)
            y = random.randint(0, self._height - 1)
            bit = random.randint(0, 3)
            if self._allowed_removal(x, y, bit):
                cell = self._get_cell(x, y)
                direction = self._get_direction(bit)
                neighbor = self._get_cell(x + direction[0], y + direction[1])
                if neighbor is None or cell is None:
                    raise MazeError("Cell not defined")
                self._remove_walls(cell, neighbor)
                amount_to_remove -= 1

    def _dfs(self) -> None:
        """Generate a perfect maze using depth-first search.

        Raises:
            MazeError: If the configured start cell is not defined.
        """
        start = self._get_cell(self._start[0], self._start[1])
        if start is None:
            raise MazeError("Start not defined")
        stack = [start]
        start.visited = True
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
    def _is_unvisited(self, node: Cell) -> bool:
        """Determine whether a cell may be visited by DFS.

        Args:
            node: Cell to inspect.

        Returns:
            True if the cell has not been visited and is not part of the
            42 pattern, otherwise False.
        """
        if node.visited is True or node.four is True or node.two is True:
            return False
        return True

    def _get_unvisited_neighbors(self, neighbors: list[Cell]) -> list[Cell]:
        """Return the unvisited neighbors from a list of cells.

        Args:
            neighbors: Neighboring cells.

        Returns:
            A list containing only unvisited cells.
        """
        unvisited = []
        for neighbor in neighbors:
            if self._is_unvisited(neighbor):
                unvisited.append(neighbor)
        return unvisited

    def _count_walls(self) -> int:
        """Count the number of internal walls in the maze.

        Raises:
            MazeError: If the configured cell is not defined.

        Returns:
            The number of east and south walls inside the maze.
        """
        count = 0
        for y in range(self._height):
            for x in range(self._width):
                cell = self._get_cell(x, y)
                if cell is None:
                    raise MazeError("Cell not defined")
                if x < self._width - 1:
                    if cell.walls >> 1 & 1:
                        count += 1
                if y < self._height - 1:
                    if cell.walls >> 2 & 1:
                        count += 1
        return count

    def _allowed_removal(self, x: int, y: int, bit: int) -> bool:
        """Determine whether a wall may be removed.

        Checks that removing the selected wall does not violate the
        imperfect maze constraints.

        Args:
            x: Cell x-coordinate.
            y: Cell y-coordinate.
            bit: Direction bit representing the wall.

        Raises:
            MazeError: If the configured cell is not defined.

        Returns:
            True if the wall may be removed, otherwise False.
        """
        cell = self._get_cell(x, y)
        if cell is None:
            raise MazeError("Cell not defined")
        direction = self._get_direction(bit)
        neighbor = self._get_cell(x + direction[0], y + direction[1])
        if neighbor is None:
            return False
        if cell.four or cell.two or neighbor.four or neighbor.two:
            return False
        if cell.walls >> bit & 1:
            if not self._3x3(cell.x, cell.y, bit):
                return True
        return False

    def _3x3_open(self, x: int, y: int) -> bool:
        """Check whether a 3x3 region is completely open internally.

        Args:
            x: Leftmost x-coordinate of the region.
            y: Topmost y-coordinate of the region.

        Returns:
            True if every internal wall of the 3x3 region is open,
            otherwise False.
        """
        # check east wall is there (only necessary in cols 0 and 1)
        for index_y in range(y, y + 3):
            for index_x in range(x, x + 2):
                cell = self._get_cell(index_x, index_y)
                if cell is None:
                    return False
                if (cell.walls >> 1) & 1:
                    return False

        # check whether south wall is there (only necessary in rows 0 and 1)
        for index_y in range(y, y + 2):
            for index_x in range(x, x + 3):
                cell = self._get_cell(index_x, index_y)
                if cell is None:
                    return False
                if (cell.walls >> 2) & 1:
                    return False

        return True

    def _3x3(self, x: int, y: int, bit: int) -> bool:
        """Determine whether removing a wall creates a 3x3 open area.

        Temporarily removes the wall, checks all affected 3x3 regions,
        and restores the wall afterwards.

        Args:
            x: Cell x-coordinate.
            y: Cell y-coordinate.
            bit: Direction bit of the wall.

        Raises:
            MazeError: If the configured start cell is not defined.

        Returns:
            True if a forbidden 3x3 region is created, otherwise False.
        """
        cell = self._get_cell(x, y)
        direction = self._get_direction(bit)
        neighbor = self._get_cell(x + direction[0], y + direction[1])
        if neighbor is None or cell is None:
            raise MazeError("Cell not defined")
        self._remove_walls(cell, neighbor)
        try:
            min_start_x = max(0, min(cell.x, neighbor.x) - 2)
            max_start_x = min(max(cell.x, neighbor.x), self._width - 3)
            min_start_y = max(0, min(cell.y, neighbor.y) - 2)
            max_start_y = min(max(cell.y, neighbor.y), self._height - 3)
            for start_y in range(min_start_y, max_start_y + 1):
                for start_x in range(min_start_x, max_start_x + 1):
                    if self._3x3_open(start_x, start_y):
                        return True
            return False
        finally:
            self._add_walls(cell, neighbor)

    # solving
    def solve(self) -> None:
        """Solve the maze and store the solution path.

        Raises:
            MazeError: If the path is not found.
        """
        path = self._bfs()
        if path is None:
            raise MazeError("Path not found.")
        self._cell_path_to_str(path)

    def _bfs(self) -> list[Cell] | None:
        """Find the shortest path using breadth-first search.

        Raises:
            MazeError: If the configured start or end cell is not defined.

        Returns:
            The shortest path as a list of cells, or None if no path
            exists.
        """
        start = self._get_cell(self._start[0], self._start[1])
        end = self._get_cell(self._end[0], self._end[1])
        if start is None or end is None:
            raise MazeError("Cell not defined")
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
                    current, neighbor
                ):
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

    def _return_path(
        self, came_from: dict[Cell, Cell], start: Cell, end: Cell
    ) -> list[Cell]:
        """Reconstruct the shortest path found by BFS.

        Args:
            came_from: Mapping from each visited cell to its predecessor.
            start: Start cell.
            end: End cell.

        Returns:
            The shortest path from start to end.
        """
        path = []
        current = end
        while current is not start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        return path

    def _allowed_entry(self, current: Cell, neighbor: Cell) -> bool:
        """Check whether movement from one cell to another is possible.

        Args:
            current: Cell currently being visited.
            neighbor: Adjacent cell to move into.

        Returns:
            True if no wall blocks movement between the cells, otherwise False.
        """
        bit = self._get_bit(current.x - neighbor.x, current.y - neighbor.y)
        if neighbor.walls >> bit & 1:
            return False
        return True

    def _cell_path_to_str(self, path: list[Cell]) -> None:
        """Convert a path of cells into an NSEW solution string.

        Args:
            path: Path returned by BFS, from end cell back to start cell.
        """
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

    # output file
    def _maze_to_str(self) -> str:
        """Convert the maze into its hexadecimal text representation.

        Returns:
            The hexadecimal maze as a multiline string.
        """
        string = ""
        for y in range(0, self._height):
            for x in range(0, self._width):
                result = "%X" % self._maze[y][x].walls
                string += result
            string += "\n"
        return string

    def output(self) -> None:
        """Write the generated maze and solution to the output file.

        Raises:
            FileError: If the output file cannot be written.
        """
        if self._file_name is None:
            name = "output_file.txt"
        else:
            name = self._file_name
        try:
            with open(name, "w") as output:
                output.write(self._structure)
                output.write("\n")
                output.write(f"{self._start[0]},{self._start[1]}\n")
                output.write(f"{self._end[0]},{self._end[1]}\n")
                output.write(self._path + "\n")
        except FileError as e:
            raise FileError(f"Output file generation error: {e}")

    # public access
    @property
    def grid(self) -> List[list[Cell]]:
        """Property method.

        Returns:
            the maze grid, list of list of cell objects
        """
        return self._maze

    @property
    def solution(self) -> str:
        """Property method.

        Returns:
            the solution string
        """
        return self._path

    # mazegen utilities
    def _get_cell(self, x: int, y: int) -> Cell | None:
        """Return the cell at the given coordinates.

        Args:
            x: Cell x-coordinate.
            y: Cell y-coordinate.

        Returns:
            The corresponding Cell if the coordinates are valid,
            otherwise None.
        """
        if x < 0 or x > self._width - 1:
            return None
        if y < 0 or y > self._height - 1:
            return None
        return self._maze[y][x]

    def _get_neighbors(self, node: Cell) -> list[Cell]:
        """Return all valid neighboring cells.

        Args:
            node: Cell whose neighbors should be returned.

        Returns:
            A list of neighboring cells.
        """
        node_neighbors = []
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x, y in neighbors:
            neighbor = self._get_cell((node.x + x), (node.y + y))
            if neighbor is not None:
                node_neighbors.append(neighbor)
        return node_neighbors

    def _remove_walls(self, current: Cell, chosen: Cell) -> None:
        """Remove the wall shared by two adjacent cells.

        Args:
            current: First cell.
            chosen: Adjacent cell.

        Raises:
            MazeError: If the cells are not adjacent in a cardinal direction.
        """
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

    def _add_walls(self, current: Cell, chosen: Cell) -> None:
        """Restore the wall shared by two adjacent cells.

        Args:
            current: First cell.
            chosen: Adjacent cell.

        Raises:
            MazeError: If the cells are not adjacent in a cardinal direction.
        """
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

    def _open_wall(self, dir: int, cell: int) -> int:
        """Open a wall in a hexadecimal wall representation.

        Args:
            dir: Direction bit to clear.
            cell: Current wall value.

        Returns:
            Updated wall value with the selected wall opened.
        """
        if dir == 0:  # north (up)
            return cell & ~0x1
        if dir == 1:  # east (right)
            return cell & ~0x2
        if dir == 2:  # south (down)
            return cell & ~0x4
        if dir == 3:  # west (left)
            return cell & ~0x8
        raise MazeError("Invalid parameters")

    def _close_wall(self, dir: int, cell: int) -> int:
        """Close a wall in a hexadecimal wall representation.

        Args:
            dir: Direction bit to set.
            cell: Current wall value.

        Returns:
            Updated wall value with the selected wall closed.
        """
        if dir == 0:  # north (up)
            return cell | (1 << 0)
        if dir == 1:  # east (right)
            return cell | (1 << 1)
        if dir == 2:  # south (down)
            return cell | (1 << 2)
        if dir == 3:  # west (left)
            return cell | (1 << 3)
        raise MazeError("Invalid parameters")

    # bit utilities
    @staticmethod
    def _get_direction(bit: int) -> tuple[int, int]:
        """Convert a wall bit into an (x, y) direction vector.

        Args:
            bit: Wall bit where 0 is north, 1 is east, 2 is south,
                and 3 is west.

        Returns:
            Direction vector matching the bit.

        Raises:
            MazeError: If the bit is not between 0 and 3.
        """
        if bit == 0:
            return (0, -1)
        elif bit == 1:
            return (1, 0)
        elif bit == 2:
            return (0, 1)
        elif bit == 3:
            return (-1, 0)
        raise MazeError("Invalid parameters")

    @staticmethod
    def _get_bit(x: int, y: int) -> int:
        """Convert a direction vector into its wall bit.

        Args:
            x: Horizontal direction offset.
            y: Vertical direction offset.

        Returns:
            Wall bit where 0 is north, 1 is east, 2 is south,
            and 3 is west.

        Raises:
            MazeError: If the direction is not one cardinal step.
        """
        if y == -1:
            return 0
        if x == 1:
            return 1
        if y == 1:
            return 2
        if x == -1:
            return 3
        raise MazeError("Invalid parameters")

    @staticmethod
    def _coord_to_direction(x1: int, x2: int, y1: int, y2: int) -> str:
        """Convert two adjacent coordinates into an NSEW direction.

        Args:
            x1: X-coordinate of the current cell.
            x2: X-coordinate of the following cell.
            y1: Y-coordinate of the current cell.
            y2: Y-coordinate of the following cell.

        Returns:
            One of "N", "E", "S", or "W".

        Raises:
            MazeError: If the coordinates do not describe a valid move.
        """
        if x1 > x2:
            return "W"
        if x1 < x2:
            return "E"
        if y1 > y2:
            return "N"
        if y1 < y2:
            return "S"
        raise MazeError("Invalid parameters")

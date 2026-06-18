#!/usr/bin/env python3

from typing import List
from mazegen import MazeGenerator
from cell import Cell


def maze_to_str(maze: List[list["Cell"]], width: int, height: int) -> str:
    string = ""
    for y in range(0, height):
        for x in range(0, width):
            result = "%X" % maze[y][x].walls
            string += result
        string += "\n"
        return string


def output(name: str, maze: str, path: str, coord: tuple[int]) -> None:
    try:
        with open(name, "w") as output:
            output.write(maze)
            output.write("\n")
            output.write(f"{coord[0]},{coord[1]}\n")
            output.write(f"{coord[2]},{coord[3]}\n")
            output.write(path + "\n")
    except Exception as e:
        print(f"Output file generation error: {e}")

if __name__ == "__main__":
    width = 20
    height = 20
    start = (0, 4)
    end = (10, 12)
    perfect = True
    seed = 233
    algorithm = 0
    mg = MazeGenerator(width, height, start, end, algorithm, perfect, seed)

    coords = [start[0], start[1], end[0], end[1]]
    coord = tuple(coords)
    print(coord)
    mg.generate()
    mg.solve()
    maze = mg.grid
    maze_string = maze_to_str(maze, width, height)
    path = mg.solution
    output("output.txt", maze_string, path, coord)
    

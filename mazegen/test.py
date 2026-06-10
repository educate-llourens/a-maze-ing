#!/usr/bin/env python3


from mazegen import MazeGenerator

if __name__ == "__main__":
    width = 16
    height = 15
    start = (0,0)
    end = (10, 5)
    algorithm = 0
    perfect = True
    seed = "haha"
    maze = MazeGenerator(width, height, start, end, algorithm, perfect, seed)
    maze.generate()

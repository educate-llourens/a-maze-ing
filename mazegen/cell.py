#!/usr/bin/python3


class Cell:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = 0xF
        self.visited = False
        self.blocked = False


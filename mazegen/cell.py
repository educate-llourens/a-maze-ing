#!/usr/bin/python3


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.walls: int = 0xF
        self.visited: bool = False
        self.blocked: bool = False
        self.four: bool = False
        self.two: bool = False

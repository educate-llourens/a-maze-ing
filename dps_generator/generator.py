#!/usr/bin/env python3

from .map import create_empty_map


def print_maze(print_map: list[list[int]]) -> None:
    for row in print_map:
        print(row)


def generator(config: dict) -> None:
    empty_map = create_empty_map(config)
    print_maze(empty_map)

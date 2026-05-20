#!/usr/bin/env python3

from dps_generator.map import create_empty_map
from visuals.display_maze import print_map


def generator(config: dict) -> None:
    map = create_empty_map(config)
    print_map(map)

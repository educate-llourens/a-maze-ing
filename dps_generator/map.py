#!/usr/bin/env python3

from typing import List
from parsing.parsing_errors import ConfigError


class MazeConfig:
    width: int
    height: int
    start: tuple
    end: tuple
    output_file: str
    perfect: bool
    seed: str | None

    def __init__(self, parsed_config: dict) -> None:
        try:
            self.width = parsed_config["WIDTH"]
            self.height = parsed_config["HEIGHT"]
            self.start = parsed_config["ENTRY"]
            self.end = parsed_config["EXIT"]
            self.output_file = parsed_config["OUTPUT_FILE"]
            self.perfect = parsed_config["PERFECT"]
            if "SEED" in parsed_config:
                self.seed = parsed_config["SEED"]
            else:
                self.seed = None
        except KeyError:
            raise ConfigError("Check that your config keys are the same as "
                              "the expected, documented structure")


def create_empty_map(parsed_config: dict) -> List[list[int]]:
    maze_settings: MazeConfig = MazeConfig(parsed_config)
    width: int = maze_settings.width
    height: int = maze_settings.height
    row: list[int] = []
    empty_map: list[list[int]] = []
    fill_value: int = 15

    def create_row(fill_value: int) -> list[int]:
        row: list[int] = []

        for cell in range(width):
            row.append(fill_value)
        return row

    for _ in range(height):
        row = create_row(fill_value)
        empty_map.append(row)
    return empty_map

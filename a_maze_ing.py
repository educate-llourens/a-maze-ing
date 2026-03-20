#!/usr/bin/env python3

import sys
from typing import List

# Error Handling --------------------------------------------------------------


class ConfigError(Exception):
    def __int__(self, msg: str):
        self.msg = msg


class InputError(Exception):
    def __int__(self, msg: str):
        self.msg = msg

# Input checking --------------------------------------------------------------


def input_checks(args: List[str]) -> None:
    pass

# Parsing ---------------------------------------------------------------------


def parse_config_file(config_file: str) -> dict:
    pass


def main() -> None:
    input_checks(sys.argv)


if __name__ == "__main__":
    main()

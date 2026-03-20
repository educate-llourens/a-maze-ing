#!/usr/bin/env python3

# Error Handling --------------------------------------------------------------

class ConfigError(Exception):
    def __int__(self, msg: str):
        self.msg = msg


class InputError(Exception):
    def __int__(self, msg: str):
        self.msg = msg

# Input checking --------------------------------------------------------------

def input_checks() -> None:
    pass

# Parsing ---------------------------------------------------------------------

def parse_config_file(config_file: str) -> dict:
    pass

def main() -> None:
    input_checks


if __name__ == "__main__":
    main()

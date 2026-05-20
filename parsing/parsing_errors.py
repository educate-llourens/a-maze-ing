#!/usr/bin/env python3

class ConfigError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Config Error: {msg}")


class InputError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Input Error: {msg}")

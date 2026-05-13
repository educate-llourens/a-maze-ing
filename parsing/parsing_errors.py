#!/usr/bin/env python3

class ConfigError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class InputError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)

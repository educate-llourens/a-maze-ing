#!/usr/bin/env python3

def user_input() -> bool:
    return False


def config_file() -> bool:
    return False


def return_value() -> bool:
    try:
        if user_input() and config_file():
            return True
    except ValueError as msg:
        raise ValueError(msg)

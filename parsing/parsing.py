#!/usr/bin/env python3

import sys
from .parsing_errors import InputError, ConfigError
from typing import Tuple


def user_input() -> bool:
    if len(sys.argv) != 2:
        raise InputError("Incorrect number of arguments")
    if sys.argv[0].endswith("a-maze-ing.py") is False:
        raise InputError("Program name is not correct. Needs to "
                         "be 'a-maze-ing.py")
    if sys.argv[1] != "config.txt":
        raise InputError("Config file name is incorrect. "
                         "It needs to be config.txt")
    return True


def convert_dict_values(dict_to_format: dict) -> dict:
    try:
        dict_to_format["WIDTH"] = int(dict_to_format["WIDTH"])
        dict_to_format["HEIGHT"] = int(dict_to_format["HEIGHT"])
        dict_to_format["ENTRY"] = tuple(
            map(int, dict_to_format["ENTRY"].split(",")))
        dict_to_format["EXIT"] = tuple(
            map(int, dict_to_format["EXIT"].split(",")))
        if dict_to_format["PERFECT"] == "True":
            dict_to_format["PERFECT"] = True
        else:
            dict_to_format["PERFECT"] = False
    except KeyError:
        raise KeyError("Could not find a config key in the dictionary")
    return dict_to_format


def config_file() -> dict:
    config_info: dict = {}

    with open(sys.argv[1], "r") as file:
        for line in file:
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            config_info[key.strip()] = value.strip()
    convert_dict_values(config_info)
    return config_info


def parsed_input_dict() -> dict:
    """It calls the input and config parser.

    Raises:
        InputError: User input errors
        ConfigError: config.txt config errors

    Returns:
        dict: a dictionary containing the config information for the
        maze generator
    """
    config_dict: dict

    user_input()
    config_dict = config_file()
    return config_dict


def check_parameters(config_dict: dict) -> None:
    entry_x: int
    entry_y: int
    exit_x: int
    exit_y: int
    width: int
    height: int

    def get_and_check_tuple(key: str) -> Tuple:
        result_x: int
        result_y: int
        result: tuple | None

        result = config_dict.get(key)
        if result is None:
            raise ConfigError(f"Could not find {key} in the config_dict")
        result_x, result_y = result
        return (result_x, result_y)

    def get_and_check_int(key: str) -> int:
        result_int: int | None

        result_int = config_dict.get(key)
        if result_int is None:
            raise ConfigError(f"Could not find {key} in config_dict")
        return int(result_int)

    entry_x, entry_y = get_and_check_tuple("ENTRY")
    exit_x, exit_y = get_and_check_tuple("EXIT")
    width = get_and_check_int("WIDTH")
    height = get_and_check_int("HEIGHT")
    if entry_x < 0 or entry_x > width:
        raise ConfigError("Entry x-coordinate out of bounds")
    if entry_y < 0 or entry_y > height:
        raise ConfigError("Entry y-coordinate out of bounds")
    if exit_x < 0 or exit_x > width:
        raise ConfigError("Exit x-coordinate out of bounds")
    if exit_y < 0 or exit_y > height:
        raise ConfigError("Exit y-coordinate out of bounds")
    if (entry_x == exit_x) and (entry_y == exit_y):
        raise ConfigError("Entry and exit cannot be the same coordinates")

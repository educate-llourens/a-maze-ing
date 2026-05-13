#!/usr/bin/env python3

import sys
from .parsing_errors import InputError, ConfigError


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
    config_dict: dict

    try:
        user_input()
    except InputError as msg:
        raise InputError(str(msg))
    try:
        config_dict = config_file()
    except KeyError as msg:
        raise ConfigError(str(msg))
    return config_dict

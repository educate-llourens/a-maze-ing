#!/usr/bin/env python3

import sys
from .parsing_errors import InputError, ConfigError
from typing import Tuple


def user_input() -> bool:
    """Parses user input from the terminal, checking the program name and
    arguments are correct.

    Raises:
        InputError(length): If the number of args is incorrect
        InputError(program name): If the program name is incorrect
        InputError(config file name): If the config file name is not correct

    Returns:
        bool: True if no errors are raised
    """
    if len(sys.argv) != 2:
        raise InputError("Incorrect number of arguments")
    if sys.argv[0].endswith("a_maze_ing.py") is False:
        raise InputError("Program name is not correct. Needs to "
                         "be 'a_maze_ing.py")
    if sys.argv[1] != "config.txt":
        raise InputError("Config file name is incorrect. "
                         "It needs to be config.txt")
    return True


def convert_dict_values(dict_to_format: dict) -> dict:
    """Converts the string values in the dictionary into the value type it
    needs to be in order to be used.

    Args:
        dict_to_format (dict): Receives the dictionary to format

    Raises:
        KeyError: If it cannot find the necessary key in the dictionary

    Returns:
        dict: The formatted dictionary with correctly typed values
    """
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
    """Reads the config file and puts all the key-value pairs into a
    dictionary. It then calls a function to convert the values into
    their correct type, then finally returns the formatted dictionary
    to be used.

    Returns:
        dict: The correctly formatted dictionary
    """
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
    """It calls the input and config parser then returns the dictionary.

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
    """Checks the entry and exit coordinates are within the map bounds as well
    as the entry and exit coordinates are not the same

    Args:
        config_dict (dict): The dictionary containing the information to check

    Raises:
        ConfigError(entry-x): entry x-coordinate is not within the map
        ConfigError(entry-y): entry y-coordinate is not within the map
        ConfigError(exit-x): exit x-coordinate is not within the map
        ConfigError(exit-y): exit y-coordinate is not within the map
        ConfigError(not same): entry and exit coordinates are the same

    Returns:
        None
    """
    entry_x: int
    entry_y: int
    exit_x: int
    exit_y: int
    width: int
    height: int

    def get_and_check_tuple(key: str) -> Tuple:
        """Gets the dictionary tuple value and checks the value is None

        Args:
            key (str): The dictionary key to get the value for

        Raises:
            ConfigError(tuple-key): could not find the key in the dictionary
            for exit or entry coordinates

        Returns:
            Tuple: The dictionary value for the given key
        """
        result_x: int
        result_y: int
        result: tuple | None

        result = config_dict.get(key)
        if result is None:
            raise ConfigError(f"Could not find {key} in the config_dict")
        result_x, result_y = result
        return (result_x, result_y)

    def get_and_check_int(key: str) -> int:
        """Gets the dictionary int value and checks the value is None

        Args:
            key (str): The dictionary key to get the value for

        Raises:
            ConfigError(int-key): could not find the key in the dictionary for
        the width or height

        Returns:
            int: The dictionary value for the given key
        """
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

#!/usr/bin/env python3

import sys
from .parsing_errors import InputError, ConfigError
from mazegen import ConfigDict


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
        raise InputError("Incorrect number of arguments, expected 2")
    if sys.argv[0].endswith("a_maze_ing.py") is False:
        raise InputError(
            "Program name is not correct. Needs to be 'a_maze_ing.py"
        )
    if sys.argv[1] != "config.txt":
        raise InputError(
            "Config file name is incorrect. It needs to be config.txt"
        )
    return True


def check_complete(raw: dict[str, str]) -> None:
    required = ["WIDTH", "HEIGHT", "EXIT", "ENTRY", "OUTPUT_FILE", "PERFECT"]

    for key in required:
        if key not in raw:
            raise ConfigError(f"Missing required key: {key}")

    for key in required:
        if raw[key] == "":
            raise ConfigError(f"Missing required value for {key}")


def convert_dict_values(dict_to_format: dict[str, str]) -> ConfigDict:
    """Converts the string values in the dictionary into the value type it
    needs to be in order to be used.

    Args:
        dict_to_format (dict): Receives the dictionary to format

    Raises:
        KeyError: If it cannot find the necessary key in the dictionary

    Returns:
        dict: The formatted dictionary with correctly typed values
    """
    formatted_dict: ConfigDict = {
        "WIDTH": 0,
        "HEIGHT": 0,
        "ENTRY": (0, 0),
        "EXIT": (0, 0),
        "OUTPUT_FILE": "output_file.txt",
        "PERFECT": False,
        "SEED": None,
    }

    check_complete(dict_to_format)
    try:
        formatted_dict["OUTPUT_FILE"] = dict_to_format["OUTPUT_FILE"]
        try:
            formatted_dict["WIDTH"] = int(dict_to_format["WIDTH"])
            formatted_dict["HEIGHT"] = int(dict_to_format["HEIGHT"])
        except ValueError:
            raise ValueError("WIDTH and HEIGHT have to be integer values")
        try:
            x1, y1 = tuple(map(int, dict_to_format["ENTRY"].split(",")))
            x2, y2 = tuple(map(int, dict_to_format["EXIT"].split(",")))
        except ValueError:
            raise ValueError(
                "Coordinate values are incorrect, expecting (int, int)"
            )
        formatted_dict["ENTRY"] = (x1, y1)
        formatted_dict["EXIT"] = (x2, y2)
        if dict_to_format["PERFECT"] == "True":
            formatted_dict["PERFECT"] = True
        elif dict_to_format["PERFECT"] == "False":
            formatted_dict["PERFECT"] = False
        else:
            raise ConfigError("PERFECT needs either 'True' or 'False'")
        try:
            dict_to_format["SEED"]
            try:
                seed = int(dict_to_format["SEED"])
            except ValueError:
                raise ValueError(
                    "Invalid seed specified, only int values allowed"
                )
            formatted_dict["SEED"] = seed
        except KeyError:
            return formatted_dict
    except KeyError:
        raise KeyError("Could not find a config key in the dictionary")
    return formatted_dict


def config_file() -> ConfigDict:
    """Reads the config file and puts all the key-value pairs into a
    dictionary. It then calls a function to convert the values into
    their correct type, then finally returns the formatted dictionary
    to be used.

    Returns:
        dict: The correctly formatted dictionary
    """
    config_info: dict[str, str] = {}

    with open(sys.argv[1], "r") as file:
        for line in file:
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ConfigError(f"{line.strip()} is not a KEY=VALUE pair. "
                                  "Please refer to the example config.txt in "
                                  "the README.md")
            key, value = line.split("=", 1)
            config_info[key.strip()] = value.strip()
    return convert_dict_values(config_info)


def parsed_input_dict() -> ConfigDict:
    """It calls the input and config parser then returns the dictionary.

    Raises:
        InputError: User input errors
        ConfigError: config.txt config errors

    Returns:
        dict: a dictionary containing the config information for the
        maze generator
    """
    config_dict: ConfigDict

    user_input()
    config_dict = config_file()
    return config_dict


def check_parameters(config_dict: ConfigDict) -> None:
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
    entry_x, entry_y = config_dict["ENTRY"]
    exit_x, exit_y = config_dict["EXIT"]
    width = config_dict["WIDTH"]
    height = config_dict["HEIGHT"]

    if entry_x < 0 or entry_x >= width:
        raise ConfigError("Entry x-coordinate out of bounds")
    if entry_y < 0 or entry_y >= height:
        raise ConfigError("Entry y-coordinate out of bounds")
    if exit_x < 0 or exit_x >= width:
        raise ConfigError("Exit x-coordinate out of bounds")
    if exit_y < 0 or exit_y >= height:
        raise ConfigError("Exit y-coordinate out of bounds")
    if (entry_x == exit_x) and (entry_y == exit_y):
        raise ConfigError("Entry and exit cannot be the same coordinates")

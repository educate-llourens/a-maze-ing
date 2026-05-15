#!/usr/bin/env python3

from parsing.parsing import (parsed_input_dict,
                             check_parameters)
from parsing.parsing_errors import (InputError,
                                    ConfigError)


def main() -> None:
    """The main function that runs the a-maze-ing project. It calls:
    1. The input and config parser, stores it in a dict
    2. The config parameter checker
    3. The maze generator and saves the .txt file
    4. Visualiser that takes in the .txt file from the generator
    5. The maze solver

    Errors: It catches and prints the following errors then exits the program:
        Parsing: InputError, ConfigError
        Generator:
        Visuals:
        Solver:
    """
    # Variables ***************************************************************
    config_dict: dict = {}

    # Parsing *****************************************************************
    try:
        config_dict = parsed_input_dict()
        check_parameters(config_dict)
    except (InputError, ConfigError) as msg:
        print(msg)
        return

    # Generator ***************************************************************

    # Visuals *****************************************************************

    # Solver ******************************************************************


if __name__ == "__main__":
    main()

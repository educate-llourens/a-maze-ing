#!/usr/bin/env python3

import sys

try:
    from parsing.parsing import parsed_input_dict, check_parameters
    from parsing.parsing_errors import InputError, ConfigError, FileError
    from visuals.display_maze import display_maze
    from mazegen import MazeGenerator, ConfigDict
    from mazegen.error import MazeError
except ModuleNotFoundError as e:
    print(f"{e}, please install this dependency before trying again.")
    sys.exit(1)


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
        Visuals: DisplayError, FileError
        Solver:
    """
    # Variables ***************************************************************
    config_dict: ConfigDict

    # Parsing *****************************************************************
    try:
        config_dict = parsed_input_dict()
        check_parameters(config_dict)
    except (InputError, ConfigError, FileError, ValueError, KeyError) as msg:
        print(msg)
        return

    # Generator ***************************************************************
    try:
        generator = MazeGenerator(config_dict)
        generator.generate()
        generator.solve()
        generator.output()
    except (ConfigError, MazeError, ValueError, FileError) as msg:
        print(msg)
        return

    # Visuals *****************************************************************
    try:
        maze_cell = generator.grid
        display_maze(config_dict, maze_cell)
    except Exception as msg:
        print(msg)
        return

    # Solver ******************************************************************


if __name__ == "__main__":
    main()

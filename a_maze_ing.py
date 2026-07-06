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
    """Run the a-maze-ing application.

    The application parses the input configuration, validates the
    parameters, generates and solves a maze, writes the output file,
    and displays the maze graphically.

    Any expected exceptions raised during parsing, generation, solving,
    or visualization are caught, reported to the user, and terminate
    the program gracefully.
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


if __name__ == "__main__":
    main()

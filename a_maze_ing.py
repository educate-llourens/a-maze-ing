#!/usr/bin/env python3

from parsing.parsing import parsed_input_dict


def main() -> None:
    config_dict: dict = {}

    try:
        config_dict = parsed_input_dict()
        # Generator
        # Visuals
        # Solver
    except (ValueError, FileNotFoundError) as msg:
        print(msg)
        return


if __name__ == "__main__":
    main()

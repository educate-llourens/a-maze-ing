#!/usr/bin/env python3

from parsing.parsing import return_value


def main() -> None:
    try:
        return_value()
        # Generator
        # Visuals
        # Solver
    except ValueError as msg:
        print(msg)
        return


if __name__ == "__main__":
    main()

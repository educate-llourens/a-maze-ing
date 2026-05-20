#!/usr/bin/env python3

# from visuals.display_errors import DisplayError


# Binary values:
#   A  | 1111 = 15
#   N  | 0111 = 7
#   E  | 1011 = 11
#   S  | 1101 = 13
#   W  | 1110 = 14
#   NE | 0011 = 3
#   NS | 0101 = 5
#   NW | 0110 = 6
#   SW | 1100 = 12
#   SE | 1001 = 9
#   EW | 1010 = 10


def print_top(row: list[int]) -> None:
    north_numbers: list[int] = [7, 3, 6, 5]

    for cell in row:
        if cell not in north_numbers:
            print("+─+", end="")
        else:
            print("   ", end="")
    print("")


def print_middle(row: list[int]) -> None:
    east_numbers: list[int] = [13, 9, 11, 3]
    west_numbers: list[int] = [14, 12, 10, 6]

    for cell in row:
        if cell in east_numbers and cell in west_numbers:
            print("   ", end="")
        elif cell in east_numbers:
            print("│  ", end="")
        elif cell in west_numbers:
            print("  │", end="")
        else:
            print("│ │", end="")
    print("")


def print_bottom(row: list[int]) -> None:
    south_numbers: list[int] = [13, 12, 9, 5]

    for cell in row:
        if cell not in south_numbers:
            print("+─+", end="")
        else:
            print("  ", end="")
    print("")


def create_empty_grid(map: list[list[int]]) -> None:
    for row in map:
        print_top(row)
        print_middle(row)


def print_map(print_map: list[list[int]]) -> None:
    create_empty_grid(print_map)


if __name__ == "__main__":
    map = [
        [5, 11, 11, 13],
        [15, 7, 15, 13],
        [15, 15, 15, 15]
    ]
    create_empty_grid(map)

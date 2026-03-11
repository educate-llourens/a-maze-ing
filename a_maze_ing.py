class MazeGenerator:
    def __init__(self):
        pass


def parse_config_file() -> dict:
    split_line: list[str]
    config_dict: dict = {}

    try:
        with open("./config.txt", "r") as config_file:
            for line in config_file:
                split_line = line.split("=", 1)
                key, value = split_line
                config_dict[key] = value
    except FileNotFoundError:
        print("Error: context.txt file not found")
        return config_dict
    except PermissionError:
        print("Error: You do not have permission to read context.txt")
        return config_dict
    return config_dict


def a_maze_ing() -> None:
    if not parse_config_file():
        return
    # Send parameters to maze generator
    # Catch errors and return


if __name__ == "__main__":
    a_maze_ing()

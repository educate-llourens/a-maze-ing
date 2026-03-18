#!/usr/bin/env python3

from a_maze_ing import parse_config_file


def test_retrieve_width():
    config_info: dict = parse_config_file()

    assert config_info["WIDTH"] == 20


def test_retrieve_all_items():
    config_info: dict = parse_config_file()

    assert config_info["HEIGHT"] == 25
    assert config_info["ENTRY"] == [0, 0]
    assert config_info["EXIT"] == [19, 14]
    assert config_info["OUTPUT_FILE"] == "maze.txt"
    assert config_info["PERFECT"] is True


def test_retrieve_commented_seed():
    conf_info: dict = parse_config_file()

    assert conf_info["SEED"] == 0


def test_retrieve_uncommented_seed():
    conf_info: dict = parse_config_file()

    assert conf_info["SEED"] == 42


def main() -> None:
    test_retrieve_width()
    test_retrieve_all_items()
    test_retrieve_commented_seed()
    test_retrieve_uncommented_seed()


if __name__ == "__main__":
    main()

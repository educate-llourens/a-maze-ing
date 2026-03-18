#!/usr/bin/env python3

import pytest
from a_maze_ing import parse_config_file


@pytest.mark.config
def test_retrieve_width():
    config_info: dict = parse_config_file()

    assert config_info["WIDTH"] == 20


@pytest.mark.config
def test_retrieve_all_items():
    config_info: dict = parse_config_file()

    assert config_info["HEIGHT"] == 25
    assert config_info["ENTRY"] == [0, 0]
    assert config_info["EXIT"] == [19, 14]
    assert config_info["OUTPUT_FILE"] == "maze.txt"
    assert config_info["PERFECT"] is True


@pytest.mark.config
def test_retrieve_commented_seed():
    conf_info: dict = parse_config_file()

    assert conf_info["SEED"] == 0


@pytest.mark.config
def test_retrieve_uncommented_seed():
    conf_info: dict = parse_config_file()

    assert conf_info["SEED"] == 42

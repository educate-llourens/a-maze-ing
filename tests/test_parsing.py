#!/usr/bin/env python3

import sys
import pytest
from parsing.parsing_errors import InputError, ConfigError
from parsing.parsing import (user_input,
                             config_file,
                             check_parameters)


@pytest.mark.input
def test_nbr_arguments(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["a-maze-ing.py", "config.txt",
                                      "nonsense"])
    with pytest.raises(InputError):
        user_input()


@pytest.mark.input
def test_input_two_correct_items(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["a-maze-ing.py", "config.txt"])
    assert user_input() is True


@pytest.mark.input
def test_input_incorrect_program_name(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["amazing.py", "config.txt"])
    with pytest.raises(InputError):
        user_input()


@pytest.mark.input
def test_input_incorrect_file(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["a-maze-ing.py", "confeg.txt"])
    with pytest.raises(InputError):
        user_input()


@pytest.mark.config
def test_read_first_line(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["a-maze-ing.py", "config.txt"])
    assert config_file()["WIDTH"] == 20


@pytest.mark.config
def test_commented_config(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["a-maze-ing.py", "config.txt"])
    config = config_file()
    assert config == {
        "WIDTH": 20,
        "HEIGHT": 25,
        "ENTRY": (0, 0),
        "EXIT": (19, 14),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True
    }


@pytest.mark.config
def test_uncommented_config(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["a-maze-ing.py",
                                      "tests/seed_config.txt"])
    config = config_file()
    assert config == {
        "WIDTH": 20,
        "HEIGHT": 25,
        "ENTRY": (0, 0),
        "EXIT": (19, 14),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True,
        "SEED": '42'
    }


@pytest.mark.config
def test_check_entry_x():
    config: dict = {}

    config = {
        "WIDTH": 20,
        "HEIGHT": 25,
        "ENTRY": (-1, 0),
        "EXIT": (19, 14),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True
    }
    with pytest.raises(ConfigError):
        check_parameters(config)


@pytest.mark.config
def test_check_entry_y():
    config: dict = {}

    config = {
        "WIDTH": 20,
        "HEIGHT": 25,
        "ENTRY": (0, 30),
        "EXIT": (19, 14),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True
    }
    with pytest.raises(ConfigError):
        check_parameters(config)


@pytest.mark.config
def test_check_exit_x():
    config: dict = {}

    config = {
        "WIDTH": 20,
        "HEIGHT": 25,
        "ENTRY": (0, 0),
        "EXIT": (-1, 14),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True
    }
    with pytest.raises(ConfigError):
        check_parameters(config)


@pytest.mark.config
def test_check_exit_y():
    config: dict = {}

    config = {
        "WIDTH": 20,
        "HEIGHT": 25,
        "ENTRY": (0, 30),
        "EXIT": (19, 30),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True
    }
    with pytest.raises(ConfigError):
        check_parameters(config)


@pytest.mark.config
def test_check_entry_matches_exit_x():
    config: dict = {}

    config = {
        "WIDTH": 20,
        "HEIGHT": 25,
        "ENTRY": (0, 15),
        "EXIT": (0, 4),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True
    }
    with pytest.raises(ConfigError):
        check_parameters(config)


@pytest.mark.config
def test_check_entry_matches_exit_y():
    config: dict = {}

    config = {
        "WIDTH": 20,
        "HEIGHT": 25,
        "ENTRY": (0, 15),
        "EXIT": (4, 15),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True
    }
    with pytest.raises(ConfigError):
        check_parameters(config)

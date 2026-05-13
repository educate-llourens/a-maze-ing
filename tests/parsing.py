#!/usr/bin/env python3

import sys
import pytest
from parsing.parsing import (user_input, config_file)


@pytest.mark.input
def input_two_correct_items(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["a-maze-ing.py", "config.txt"])
    assert user_input() is True


@pytest.mark.input
def input_incorrect_program_name(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["amazing.py", "config.txt"])
    with pytest.raises(ValueError):
        user_input()


@pytest.mark.input
def input_incorrect_file(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["a-maze-ing.py", "confeg.txt"])
    with pytest.raises(FileNotFoundError):
        user_input()


@pytest.mark.input
def file_name():
    assert sys.argv[0].endswith("a-maze-ing.py")


@pytest.mark.input
def config_file_name():
    assert sys.argv[1] == "config.txt"


@pytest.mark.config
def read_first_line():
    assert config_file()["WIDTH"] == 20


@pytest.mark.config
def commented_config():
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
def uncommented_config():
    config = config_file()
    assert config == {
        "WIDTH": 20,
        "HEIGHT": 25,
        "ENTRY": (0, 0),
        "EXIT": (19, 14),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True,
        "SEED": 42
    }

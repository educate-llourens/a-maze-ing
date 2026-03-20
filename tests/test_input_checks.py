#!/usr/bin/env python3

import pytest
from a_maze_ing import input_checks
from a_maze_ing import InputError


@pytest.fixture
def input_two_arg(monkeypatch):
    monkeypatch.setattr("sys.argv", ["./program_name", "requirements.txt",
                                     "config.txt"])


@pytest.fixture
def incorrect_argv1(monkeypatch):
    monkeypatch.setattr("sys.argv", ["./program_name", "a_maze_ing.py"])


@pytest.fixture
def correct_args(monkeypatch):
    monkeypatch.setattr("sys.argv", ["./program_name", "config.txt"])


@pytest.fixture
def incorrect_file(monkeypatch):
    monkeypatch.setattr("sys.argv", ["./program_name", "confeg.txt"])


@pytest.mark.input
def file_not_found(incorrect_file):
    with pytest.raises(FileNotFoundError, match="FileNotFound Error: Could not"
                       "find config.txt"):
        input_checks()


@pytest.mark.input
def test_argc_is_one(input_one_arg):
    with pytest.raises(InputError, match="InputError: The number of arguments"
                       "is not 1"):
        input_checks()


@pytest.mark.input
def test_first_argv(incorrect_argv1):
    with pytest.raises(InputError, match="InputError: First argument is not"
                       "config.txt"):
        input_checks()


@pytest.mark.input
def correct_input(correct_args):
    result = input_checks()
    assert result is not None

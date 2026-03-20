#!/usr/bin/env python3

import sys
import pytest
from a_maze_ing import input_checks


@pytest.fixture
def input_one_arg(monkeypatch):
    monkeypatch.setattr("sys.argv", ["./program_name"])


@pytest.fixture
def incorrect_argv1(monkeypatch):
    monkeypatch.setattr("sys.argv", ["./program_name", "amazed.py",
                                     "config.txt"])


@pytest.fixture
def incorrect_argv2(monkeypatch):
    monkeypatch.setattr("sys.argv", ["./program_name", "a_maze_ing.py",
                                     "requirements.txt"])


@pytest.fixture
def correct_args(monkeypatch):
    monkeypatch.setattr("sys.argv", ["./program_name", "a_maze_ing.py",
                                     "config.txt"])


@pytest.mark.input
def test_argc_is_two(input_one_arg):
    with pytest.raises(InputError, match="InputError: The number of arguments"
                       "is not 2"):
        input_checks()


@pytest.mark.input
def test_first_argv(incorrect_argv1):
    with pytest.raises(InputError, match="InputError: First argument is not"
                       "a_maze_ing.py file"):
        input_checks()


@pytest.mark.input
def test_second_argv():
    with pytest.raises(InputError, match="InputError: Second argument is not"
                       "config.txt"):
        input_checks()


@pytest.mark.input
def correct_input(correct_args):
    result = input_checks()
    assert result is not None

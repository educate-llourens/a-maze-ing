#!/usr/bin/env python3

import pytest
from a_maze_ing import input_checks
from a_maze_ing import InputError


@pytest.mark.input
def test_file_not_found():
    with pytest.raises(FileNotFoundError, match="FileNotFound Error: Could not"
                       "find config.txt"):
        input_checks(["./program_name", "confeg.txt"])


@pytest.mark.input
def test_argc_is_one():
    with pytest.raises(InputError, match="InputError: The number of arguments"
                       "is not 1"):
        input_checks(["./program_name"])


@pytest.mark.input
def test_first_argv():
    with pytest.raises(InputError, match="InputError: First argument is not"
                       "config.txt"):
        input_checks(["./program_name", "a_maze_ing.py"])


@pytest.mark.input
def test_correct_input():
    result = input_checks(["./program_name", "config.txt"])
    assert result is not None

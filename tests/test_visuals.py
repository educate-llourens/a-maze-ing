#!/usr/bin/env python3

import pytest
from visuals.display_errors import DisplayError
from visuals.read_map import run_display


@pytest.mark.visuals
def test_read_hex_map() -> None:
    print

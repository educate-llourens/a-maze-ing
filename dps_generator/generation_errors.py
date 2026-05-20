#!/usr/bin/env python3

class GenerationError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"GenerationError: {msg}")

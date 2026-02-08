MAIN= a_maze_ing.py
CONFIG= config.txt
VENV_DIR= venv
BIN_DIR= $(VENV_DIR)/bin
PYTHON= $(BIN_DIR)/python3
PIP= $(BIN_DIR)/pip
MYPY_FLAGS= --warn-return-any \
			--warn-unused-ignore \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs

all: run

install:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install flake8
	$(PIP) install mypy

run:
	$(PYTHON) $(MAIN) $(CONFIG)


debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)


clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf venv
# 	This is for the pytest library later
	rm -rf .pytest_cache

lint:
	$(BIN_DIR)/flake8 .
	$(PYTHON) -m mypy . $(MYPY_FLAGS)

lint-strict:
	$(BIN_DIR)/flake8 .
	$(PYTHON) -m mypy . --strict
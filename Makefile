MAIN= a_maze_ing.py
CONFIG= config.txt
VENV_DIR= amazeing_venv
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
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

test:
	cd $(VENV_DIR)
	$(PIP) install pytest

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf $(VENV_DIR)
	rm -rf .pytest_cache

lint:
	flake8
	$(PYTHON) -m mypy . $(MYPY_FLAGS)

lint-strict:
	flake8
	$(PYTHON) -m mypy . --strict
MAIN= a_maze_ing.py
CONFIG= config.txt
VENV_DIR= maze_venv
BIN_DIR= $(VENV_DIR)/bin
PYTHON= $(BIN_DIR)/python3
PIP= $(BIN_DIR)/pip
MYPY_FLAGS= --warn-return-any \
			--warn-unused-ignore \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs

all: run

build:
	python3 -m build
	mv dist/mazegen-*.whl .

install:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache

bonfire:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf $(VENV_DIR)
	rm -rf .pytest_cache

lint:
	flake8
	mypy . $(MYPY_FLAGS)

lint-strict:
	flake8
	mypy . --strict

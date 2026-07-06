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
	rm -r dist mazegen.egg-info

install:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	tar -xvf mlx_CLXV-2.2.tgz
	cd mlx_CLXV && make
	$(PIP) install mlx_CLXV/mlx-*.whl
	$(PIP) install mazegen-*.whl

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
	rm -rf mlx_CLXV

lint:
	flake8 --exclude=maze_venv,mlx_CLXV
	mypy --exclude 'mlx_CLXV/|maze_venv/' . $(MYPY_FLAGS)


lint-strict:
	flake8 --exclude=maze_venv,mlx_CLXV
	mypy --exclude 'mlx_CLXV/|maze_venv/' . --strict


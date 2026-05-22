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

install:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	sudo apt-get install -y libxext-dev libx11-dev libbsd-dev
	git clone https://github.com/42Paris/minilibx-linux.git && cd minilibx-linux && make
	gcc -shared -fPIC -o libmlx.so $(ls *.c | grep -v mlx_lib_xpm.c) -lX11 -lXext -lbsd
	cd ..

pacman:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	sudo pacman -S libxext libx11 libbsd
	git clone https://github.com/42Paris/minilibx-linux.git && cd minilibx-linux && make
	gcc -shared -fPIC -o libmlx.so $(ls *.c | grep -v mlx_lib_xpm.c) -lX11 -lXext -lbsd
	cd ..

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

test:
	pytest

test-input:
	pytest -m input

test-config:
	pytest -m config

test-visuals:
	pytest -m visuals

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache

bonfire:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf $(VENV_DIR)
	rm -rf .pytest_cache
	rm -rf minilibx-linux

lint:
	flake8
	python3 -m mypy . $(MYPY_FLAGS)

lint-strict:
	flake8
	$(PYTHON) -m mypy . --strict
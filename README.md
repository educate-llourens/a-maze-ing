*This project has been created as part of the 42 curriculum by odschreu, lelouren*

# a_maze_ing

![Screenshot](visuals/files/maze_screenshot.png)

## Description

a_maze_ing is a maze generator project for the 42 core curriculum. It is a python written program that allows you to generate a maze and its shortest path solution. The maze is visualized with the MiniLibX library. The maze generator will allow you to set entry and exit points, as well as whether you would like a perfect or imperfect maze generated. You can also regenerate or reproduce the same maze by the use of a seed.
# a_maze_ing

![Screenshot](visuals/files/maze_screenshot.png)

## Description

a_maze_ing is a maze generator project for the 42 core curriculum. It is a python written program that allows you to generate a maze and its shortest path solution. The maze is visualized with the MiniLibX library. The maze generator will allow you to set entry and exit points, as well as whether you would like a perfect or imperfect maze generated. You can also regenerate or reproduce the same maze by the use of a seed.

## Goals of this project
**Main goals** <br>
[✔] Create a maze generator from a config file <br>
[✔] Generate a perfect maze  <br>
[✔] Output the maze as a hexadecimal representation  <br>
[✔] Create a visual representation of the maze and its shortest path solution  <br>
[✔] Ensure it is appropriately packaged for reusing later <br>

**Extras** <br>
[✔] Visualise the maze with mlx <br>
[✔] Change the whole theme of the maze and not just the colour <br>
[✔] Regenerate the same maze with a single key press <br>
[✔] Generate a new maze with a single key press <br>
[✔] Created a separate, movable intrsuctions window for interacting with the maze generator <br>

# Instructions

## Setup

1. Install the project and its dependencies:

   ```bash
   make install
   ```

   This command:

   * Creates the Python virtual environment (`maze_venv`)
   * Upgrades `pip`
   * Installs the required Python packages
   * Extracts and builds the `mlx` wrapper
   * Installs both the `mlx` and `mazegen` wheel packages into the virtual environment

2. Activate the virtual environment:

   ```bash
   source maze_venv/bin/activate
   ```

3. Run the program:

   ```bash
   python3 a_maze_ing.py config.txt
   ```

To generate different mazes, modify `config.txt` or provide a different configuration file.

## Makefile Commands

| Command            | Description                                                                                                          |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| `make install`     | Sets up the virtual environment and installs all project dependencies.                                               |
| `make build`       | Rebuilds the `mazegen` package and generates a new `.whl` file. Run this after making changes to the package source. |
| `make run`         | Runs the program using the default configuration file.                                                               |
| `make debug`       | Launches the program in the Python debugger (`pdb`).                                                                 |
| `make lint`        | Runs `flake8` and `mypy` with the project's standard type-checking configuration.                                    |
| `make lint-strict` | Runs `flake8` and `mypy` in strict mode.                                                                             |
| `make clean`       | Removes Python cache directories and temporary files.                                                                |
| `make bonfire`     | Removes the virtual environment along with all caches for a complete cleanup.                                        |

# Resources

## Website links
### Using Git for team work

1. <https://devot.team/blog/git-collaboration>
2. <https://github.com/hei1sme/git-github-book>
3. <https://dev.to/gladyspascual/a-beginner-s-guide-to-using-git-when-working-with-a-team-for-the-first-time-1hba>

### Makefiles

1. <https://earthly.dev/blog/python-makefile/>

### Maze generation

1. <https://www.youtube.com/watch?v=184Oair5iys>
2. <https://en.wikipedia.org/wiki/Maze_generation_algorithm>
3. <https://stackoverflow.com/questions/38502/whats-a-good-algorithm-to-generate-a-maze>
4. <https://professor-l.github.io/mazes/>
5. <https://dchakarov.com/blog/maze-algorithms/>
6. <https://uca.hal.science/hal-03174952v1/document>

## Other

1. Peers at Codam to ask about their implementations / approaches
2. YouTube tutorials on maze generation (other programming languages but similar algorithm implementations)
3. For python itself: the Python modules from the Core Curriculum at Codam
4. ClaudeAI as a tutor, asking to explain concepts and to be used as a guide of where to look (not used to write code)

# Additional Information


## Structure and format of the config file

```
WIDTH=20
HEIGHT=25
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output.txt
PERFECT=True
#SEED=42
```

| **Key** | **Description** |
| ----------- | ----------- |
| WIDTH | The width that the maze needs to be |
| HEIGHT | The height that the maze needs to be |
| ENTRY | The entry coordinates for the maze |
| EXIT | The exit coordinates for the maze |
| OUTPUT_FILE | The name of the file for the generated maze information |
| PERFECT | A boolean for if the maze should be a perfect maze |
| SEED | A seed number if you want to regenerate the maze with a specific seed |

## Maze generation Algorithm
**Depth-First Search (DFS)** <br>
DFS is a graph/tree traversal algorithm. Starting from a node, it goes as deep as possible down one path before backtracking. 

**Why we chose it** <br>
- It is good for perfect mazes because of it's depth first approach
- Every time it wants to move to another cell it randomises which unvisited cell it will visit next. This makes it reliably random
- It is simple to understand and implement
- It has fewer and longer dead ends making it more interesting to solve

## Reusable code

## Using `mazegen`

Once the `mazegen` package is installed (either in your Python environment or a virtual environment), import it into your project using either of the following:

```python
import mazegen
```

or

```python
from mazegen import MazeGenerator
```

Both options provide access to the `MazeGenerator` class. Using `import mazegen` also imports the `ConfigDict` type, which can be useful for type hinting when creating configuration dictionaries.

### Creating a `MazeGenerator`

Create a `MazeGenerator` by passing a configuration dictionary to the constructor:

```python
generator = MazeGenerator(config)
```

The configuration dictionary specifies maze dimensions, generation options, start/end positions, output settings, and other generation parameters.

### Public Methods

| Method       | Description                                                                                                                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `generate()` | Generates a maze using a depth-first search algorithm. If enabled, it applies the optional 42 pattern, optionally converts the maze into an imperfect maze, and stores the final hexadecimal maze representation. |
| `solve()`    | Solves the generated maze using breadth-first search and stores the solution path. Raises a `MazeError` if no valid path exists.                                                                                  |
| `output()`   | Writes the generated maze, start and end coordinates, and solution path to the configured output file. If no filename is specified, the output is written to `output_file.txt`.                                   |

### Properties

| Property   | Description                                                                                                           |
| ---------- | --------------------------------------------------------------------------------------------------------------------- |
| `grid`     | Returns the maze as a two-dimensional list of `Cell` objects, allowing direct access to the generated maze structure. |
| `solution` | Returns the solution path as a string after `solve()` has been called.                                                |


## Team and project management
**odschreu** <br>
- Maze Generator
- Maze Solver
- Output file from the maze generator and solver
- Packaging of the maze generator as per the subject requirements
- Seeking and resolving edge cases
- Connecting the maze generator to the visualisation
- Error handling for the maze generator and parsing
- Contributing to the README.md
- Ensuring it is mypy and flake8 complient

**lelouren** <br>
- Parsing
- Mlx visualisation of the maze
- Error handling for visualisation and parsing
- Creating the Makefile and requirements.txt
- Creating foundations for the README.md

### Project planning
We met once per week to discuss our progress and what needed to be done for the coming week

### What worked well
- Meeting at least once a week
- One Github repository where we are both collaborators
- Splitting of the tasks according to generation or visualisation
- A simple main file that delegates the different sections of the project. Each section then has its own folder with files and error handling
- Meeting at least once a week
- One Github repository where we are both collaborators
- Splitting of the tasks according to generation or visualisation
- A simple main file that delegates the different sections of the project. Each section then has its own folder with files and error handling

### What can be improved
- Do the check parameters before returning the dict to the main
- Create a class instead of a dict because fetching information from a dict has a high risk of failing if there is a key mismatch
- Have one class with all the necessary information instead of a class that gets absorbed by another class, that gets absorbed again.
- Reading from only the output file instead of the config file as well

### Tools


- `pytest` — unit testing
- `mypy` — static type checking
- `flake8` — code style linting
- `make` — task automation
- `pip` — package management
- `venv` — virtual environment isolation
- `build` / `setuptools` — packaging the maze generator
- `minilibx-linux` — graphical display (C library loaded via ctypes)
- `Claude` — concept explanation, debugging, project planning

#### AI usage


Claude:


- Breaking down project requirements into daily tasks
- Explaining concepts such as ctypes and algorithms
- Formatting
- Giving structure to the README and helped polishing the README

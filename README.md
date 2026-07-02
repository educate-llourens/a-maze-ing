*This project has been created as part of the 42 curriculum by odschreu, lelouren*

# a_maze_ing

![Screenshot](visuals/files/maze_screenshot.png)

## Description

a_maze_ing is a maze generator project for the 42 core curriculum. It is a python written program that allows you to generate a maze and its shortest path solution. The maze is visualized with the MiniLibX library. The maze generator will allow you to set entry and exit points, as well as whether you would like a perfect or imperfect maze generated. You can also regenerate or reproduce the same maze by the use of a seed.

## Goals of this project

**Main goals of the project** <br>
[✓] Create a maze generator from a config file  <br>
[✓] Generate a perfect maze  or imperfect maze <br>
[✓] Output the maze as a hexadecimal representation  in a .txt file <br>
[✓] Create a visual representation of the maze and its shortest path solution <br>
[✓] Ensure it is appropriately packaged for reusing later <br>

**Extras** <br>
[✓] Visualisation with mlx <br>
[✓] Can change the whole theme of the maze and not just the colour <br>
[✓] Can regenerate the same maze with the click of a key<br>
[✓] Shows and hides the solution path <br>
[✓] Can regenerate different mazes with the click of a key <br>
[✓] Separate window with clear instructions <br>

# Instructions

# Resources

## Using Git for team work

1. <https://devot.team/blog/git-collaboration>
2. <https://github.com/hei1sme/git-github-book>
3. <https://dev.to/gladyspascual/a-beginner-s-guide-to-using-git-when-working-with-a-team-for-the-first-time-1hba>

## Makefiles

1. <https://earthly.dev/blog/python-makefile/>

## Maze generation

1. <https://www.youtube.com/watch?v=184Oair5iys>
2. <https://en.wikipedia.org/wiki/Maze_generation_algorithm>
3. <https://stackoverflow.com/questions/38502/whats-a-good-algorithm-to-generate-a-maze>
4. <https://professor-l.github.io/mazes/>
5. <https://dchakarov.com/blog/maze-algorithms/>
6. <https://uca.hal.science/hal-03174952v1/document>

# Additional Information

## Structure and format of the config file

**Example config structure**
```
WIDTH=20
HEIGHT=25
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output.txt
PERFECT=True
#SEED=42
```

**Descriptions**
| Key | Description |
| ----------- | ----------- |
| WIDTH | Width that the maze should be |
| HEIGHT | Height that the maze should be |
| ENTRY | The entry coordinates for the maze |
| EXIT | The exit coordinates for the maze |
| OUTPUT_FILE | The file to output the maze to |
| PERFECT | A boolean indicating if it should be a perfect maze |
| SEED | Specifies a seed if applicable |


## Maze generation Algorithm
### Why we chose it

## Reusable code

## Team and project management
**Odin**
- Maze Generator
- Maze Solver
- Output file from the maze generator and solver
- Packaging of the maze generator as per the subject requirements
- Seeking and resolving edge cases
- Connecting the maze generator to the visualisation
- Error handling for the maze generator and parsing
- Contributing to the README.md

**Leandra**
- Parsing
- Mlx visualisation of the maze
- Error handling for visualisation and parsing
- Creating the Makefile and requirements.txt
- Creating foundations for the README.md

### Project planning
We met on a weekly basis to discuss what we have done and what we need to do that week. 

### What worked well
- Meeting at least once a week
- One Github repository where we are both collaborators
- Splitting of the tasks according to generation or visualisation
- A simple main file that delegates the different sections of the project. Each section then has its own folder with files and error handling

### What can be improved
**Parsing**
- Do the check parameters before returning the dict to the main <br>
- Create a class instead of a dict because fetching information from a dict has a high risk of failing if there is a key mismatch

**Maze generation** <br>

**Visualisation**
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

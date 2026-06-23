from visuals.display_classes import DrawingData, MazeInfo, Direction
from time import sleep

# Functions in file -----------------------------------------------------------
# 1.  has_north_wall
# 2.  has_west_wall
# 3.  fill_wall
# 4.  draw_top_border
# 5.  draw_left_border
# 6.  draw_internal_walls
# 7.  draw_right_border
# 8.  draw_bottom_border
# 9.  draw_entry
# 10. draw_exit
# 11. draw_steps
# -----------------------------------------------------------------------------


def has_north_wall(cell_value: int) -> bool:
    return bool(cell_value & Direction.NORTH.value)


def has_west_wall(cell_value: int) -> bool:
    return bool(cell_value & Direction.WEST.value)


def fill_wall(data: DrawingData, start_x: int, start_y: int, width: int,
              height: int) -> None:
    for offset_y in range(0, height, data.image.wall_height):
        for offset_x in range(0, width, data.image.wall_width):
            sleep(0.001)
            if data.alternate is False:
                data.mlx.mlx_put_image_to_window(
                    data.mlx_ptr,
                    data.window_ptr,
                    data.image.wall_ptr,
                    start_x + offset_x,
                    start_y + offset_y,
                )
            else:
                data.mlx.mlx_put_image_to_window(
                    data.mlx_ptr,
                    data.window_ptr,
                    data.image.alt_wall_ptr,
                    start_x + offset_x,
                    start_y + offset_y,
                )


def draw_top_border(data: DrawingData):
    top_y = 0
    for col_index in range(data.cols):
        col_x = col_index * data.passage
        fill_wall(data, col_x, top_y, data.wall, data.wall)
        fill_wall(data, col_x + data.wall, top_y, data.inner, data.wall)
    fill_wall(data, data.cols * data.passage, top_y, data.wall, data.wall)


def draw_left_border(data: DrawingData):
    left_x = 0
    for row_index in range(data.rows):
        row_y = row_index * data.passage
        fill_wall(data, left_x, row_y, data.wall, data.wall)
        fill_wall(data, left_x, row_y + data.wall, data.wall, data.inner)
    fill_wall(data, left_x, data.rows * data.passage, data.wall, data.wall)


def draw_internal_walls(data: DrawingData):
    for row_index, cell_list in enumerate(data.maze):
        row_y = row_index * data.passage
        for col_index, cell_value in enumerate(cell_list):
            col_x = col_index * data.passage

            # Corner joint at the top-left of the cell
            fill_wall(data, col_x, row_y, data.wall, data.wall)

            # Horizontal segment across the top of the cell interior
            if has_north_wall(cell_value):
                fill_wall(data, col_x + data.wall, row_y, data.inner,
                          data.wall)

            # Vertical segment down the left of the cell interior
            if has_west_wall(cell_value):
                fill_wall(data, col_x, row_y + data.wall, data.wall,
                          data.inner)


def draw_entry(data: DrawingData, drawing: MazeInfo):
    row_index, col_index = drawing.entry_coord
    col_x = col_index * data.passage
    row_y = row_index * data.passage
    if data.alternate is False:
        data.mlx.mlx_put_image_to_window(
            data.mlx_ptr,
            data.window_ptr,
            data.image.start_ptr,
            col_x + data.wall,
            row_y + data.wall,
        )
    else:
        data.mlx.mlx_put_image_to_window(
            data.mlx_ptr,
            data.window_ptr,
            data.image.alt_start_ptr,
            col_x + data.wall,
            row_y + data.wall,
        )


def draw_right_border(data: DrawingData) -> None:
    right_x = data.cols * data.passage
    for row_index in range(data.rows):
        row_y = row_index * data.passage
        fill_wall(data, right_x, row_y, data.wall, data.wall)
        fill_wall(data, right_x, row_y + data.wall, data.wall, data.inner)
    fill_wall(data, right_x, data.rows * data.passage, data.wall, data.wall)


def draw_bottom_border(data: DrawingData) -> None:
    bottom_y = data.rows * data.passage
    for col_index in range(data.cols):
        col_x = col_index * data.passage
        fill_wall(data, col_x, bottom_y, data.wall, data.wall)
        fill_wall(data, col_x + data.wall, bottom_y, data.inner, data.wall)
    fill_wall(data, data.cols * data.passage, bottom_y, data.wall, data.wall)


def draw_exit(data: DrawingData, drawing: MazeInfo) -> None:
    row_index, col_index = drawing.exit_coord
    col_x = col_index * data.passage
    row_y = row_index * data.passage
    sleep(0.05)
    if data.alternate is False:
        data.mlx.mlx_put_image_to_window(
            data.mlx_ptr,
            data.window_ptr,
            data.image.end_ptr,
            col_x + data.wall,
            row_y + data.wall,
        )
    else:
        data.mlx.mlx_put_image_to_window(
            data.mlx_ptr,
            data.window_ptr,
            data.image.alt_end_ptr,
            col_x + data.wall,
            row_y + data.wall,
        )


def draw_steps(data: DrawingData, coordinates: tuple, next_step: str, entry: tuple) -> None:
    inner_x: int
    inner_y: int

    col_index, row_index = coordinates
    col_x = col_index * data.passage
    row_y = row_index * data.passage
    inner_x = col_x + data.inner
    inner_y = row_y + data.inner
    if coordinates != entry:
        data.mlx.mlx_put_image_to_window(
            data.mlx_ptr,
            data.window_ptr,
            data.image.steps_ptr,
            col_x + data.wall,
            row_y + data.wall,
        )
    col_x = col_index * data.passage
    row_y = row_index * data.passage
    if next_step == "N":
        inner_y = inner_y - data.wall
    elif next_step == "E":
        inner_x = inner_x + data.wall
    elif next_step == "S":
        inner_y = inner_y + data.wall
    elif next_step == "W":
        inner_x = inner_x - data.wall
    data.mlx.mlx_put_image_to_window(
        data.mlx_ptr,
        data.window_ptr,
        data.image.steps_ptr,
        inner_x,
        inner_y,
    )

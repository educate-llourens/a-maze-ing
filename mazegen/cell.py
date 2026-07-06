class Cell:
    """Represent a single cell in the maze.

    Each cell stores its position, wall configuration, traversal state,
    and whether it belongs to the optional 42 pattern.
    """
    def __init__(self, x: int, y: int) -> None:
        """Initialize a maze cell.

        Args:
            x: Horizontal coordinate of the cell.
            y: Vertical coordinate of the cell.
        """
        self.x: int = x
        self.y: int = y
        self.walls: int = 0xF
        self.visited: bool = False
        self.blocked: bool = False
        self.four: bool = False
        self.two: bool = False

class MazeError(BaseException):
    """Shows errors related to a maze generation issue

    Args:
        BaseException: base exception class.
    """

    def __init__(self, msg: str) -> None:
        """Creates a Mlx error

        Args:
            msg (str): Message to display if the error happens
        """
        super().__init__(f"Maze Error: {msg}")

class ConfigError(Exception):
    """Exception raised for invalid maze configuration."""

    def __init__(self, msg: str):
        """Initialize the exception.

        Args:
            msg: Description of the configuration error.
        """
        super().__init__(f"Config Error: {msg}")


class InputError(Exception):
    """Exception raised for invalid user input."""

    def __init__(self, msg: str):
        """Initialize the exception.

        Args:
            msg: Description of the input error.
        """
        super().__init__(f"Input Error: {msg}")


class FileError(Exception):
    """Exception raised for file-related errors."""

    def __init__(self, msg: str):
        """Initialize the exception.

        Args:
            msg: Description of the file error.
        """
        super().__init__(f"File Error: {msg}")

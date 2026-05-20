class DisplayError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Display Error: {msg}")

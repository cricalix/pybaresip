class BaresipNotFound(Exception):
    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        return f"Executable for 'baresip' could not be found ({self.path})"

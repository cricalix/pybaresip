class FileNotFound(Exception):
    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        return f"pybaresip could not find '{self.path}'"


class BaresipNotFound(FileNotFound):
    def __str__(self) -> str:
        return f"Executable for 'baresip' could not be found ({self.path})"


class BaresipConfigNotFound(FileNotFound):
    def __str__(self) -> str:
        return f"Configuration for 'baresip' could not be found ({self.path})"

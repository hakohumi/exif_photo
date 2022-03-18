
from pathlib import Path


class Marker:
    def __init__(self, filepath: Path, location: tuple[float, float]):
        self.filepath: Path = filepath
        self.location: tuple[float, float] = location

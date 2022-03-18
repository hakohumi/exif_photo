
from pathlib import Path

from exif_reader.exif_reader import ExifImage


class ImageMarker:
    def __init__(self, filepath: Path):
        self.filepath: Path = filepath
        self.exif_image = ExifImage(filepath)
        self.location: tuple[float,
                             float] | None = self.exif_image.get_geo_deg()

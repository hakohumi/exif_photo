
from pathlib import Path

from exif_reader.exif_reader import ExifImage


class ImageMarker:
    def __init__(self, filepath: Path):
        self.file_path: Path = filepath
        self.exif_image = ExifImage(filepath)
        self.location: tuple[float,
                             float] | None

        try:
            self.location = self.exif_image.get_geo_deg()
        except Exception:
            self.location = None

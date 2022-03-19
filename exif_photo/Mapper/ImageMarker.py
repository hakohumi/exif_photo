
from pathlib import Path

from exif_photo.Reader.exif_reader import ExifImage


class ImageMarker:
    def __init__(self, file_path: Path):
        self.file_path: Path = file_path
        self.exif_image = ExifImage(file_path)
        self.location: tuple[float,
                             float] | None

        try:
            self.location = self.exif_image.get_geo_deg()
        except Exception:
            self.location = None

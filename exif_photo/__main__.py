# コマンドライン引数
import sys

# ファイル操作
from pathlib import Path

from exif_photo.Mapper.ImageMarker import ImageMarker
from exif_photo.Mapper import Mapper


def search_file(search_dir: str, pattern: str) -> list[str]:
    path = Path(search_dir)
    filepaths: list[Path] = list(path.glob(pattern))

    return [path.as_posix() for path in filepaths]


if __name__ == "__main__":

    def check_search_dir_in_arg() -> str:
        if len(sys.argv) == 1:
            print("検索ディレクトリの指定がないため、実行ディレクトリ下のimagesディレクトリ内を検索します。")
            return "./images/"
        elif len(sys.argv) == 2:
            return Path(sys.argv[1]).as_posix()
        else:
            raise ValueError

    def make_map(file_paths: list[str]):
        image_markers: list[ImageMarker] = [
            ImageMarker(Path(path)) for path in file_paths]

        Mapper.make_map(image_markers)

    def _main():
        file_paths: list[str] = []
        search_dir: str
        try:
            search_dir = check_search_dir_in_arg()
        except ValueError:
            print("コマンドライン引数が不正です。")
            return

        file_paths.extend(search_file(search_dir, "**/*.png"))
        file_paths.extend(search_file(search_dir, "**/*.jpg"))

        if not file_paths:
            print(f"{search_dir}は画像ファイルが存在しません。")
            return

        make_map(file_paths)

        print("finish")

    _main()

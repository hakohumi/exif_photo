from typing import Any
from exif_photo.ImageMarker import ImageMarker
# コマンドライン引数
import sys

# ファイル操作
from pathlib import Path

import webbrowser

import folium
from folium import plugins


def first_true(iterable, default: Any = None, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)


def search_file(search_dir: str, pattern: str) -> list[str]:
    path = Path(search_dir)
    filepaths: list[Path] = list(path.glob(pattern))

    return [path.as_posix() for path in filepaths]


if __name__ == "__main__":

    def check_search_dir_in_arg() -> str | None:
        if len(sys.argv) == 1:
            print(sys.argv)
            return None
        elif len(sys.argv) == 2:
            print(sys.argv)
            return Path(sys.argv[1]).as_posix()
        else:
            raise ValueError

    def _main():
        filepaths: list[str] = []
        search_dir: str = "./images/"

        filepaths.extend(search_file(search_dir, "**/*.png"))
        filepaths.extend(search_file(search_dir, "**/*.jpg"))

        if not filepaths:
            print(f"{search_dir}は画像ファイルが存在しません。")
        if not filepaths:
            print("画像ファイルが見つかりませんでした。")
            return

        # 画像ファイルのマーカーオブジェクトの作成
        image_markers: list[ImageMarker] = [
            ImageMarker(Path(path)) for path in filepaths]

        image_markers = [
            marker for marker in image_markers if marker.location is not None]

        print()

        # マップ作成

        location: tuple[float, float]

        _location: ImageMarker | None = first_true(
            image_markers, None, lambda x: x.location is not None)

        if (_location is not None and _location.location is not None):
            location = _location.location
        else:
            print("locationが不正です")
            return

        print(location)

        map = folium.Map(
            location=location,
            zoom_start=20)

        # マーカークラスターのレイヤーを作成
        marker_cluster = plugins.MarkerCluster().add_to(map)

        for marker in image_markers:
            file_name = marker.file_path.name
            file_path = marker.file_path.as_posix()
            print(file_path)
            # ポップアップの作成(「show=True」で常に表示)
            p_up = folium.Popup(
                html=f"<center>{file_name}<br><img width='100%' src='{file_path}'></center>",
                min_width=0,
                max_width=1000,
                show=True)

            # 地図オブジェクトにプロット
            folium.Marker(
                location=marker.location,
                popup=p_up).add_to(marker_cluster)

        # 地図表示
        map.save('index.html')

        webbrowser.open("index.html")

        print("finish")

    def marker_help():
        help(plugins.MarkerCluster)

    _main()

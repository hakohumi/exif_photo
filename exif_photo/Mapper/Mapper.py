from exif_photo.util import first_true
from exif_photo.Mapper.ImageMarker import ImageMarker

import folium
from folium import plugins

import webbrowser


def make_map(image_markers: list[ImageMarker]):
    # 画像ファイルのマーカーオブジェクトの作成

    # 画像ファイル内のGPSInfoにlocation情報がないマーカーは除外する。
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


def marker_help():
    help(plugins.MarkerCluster)

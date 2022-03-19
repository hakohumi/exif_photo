from exif_photo.util import first_true
from exif_photo.Mapper.ImageMarker import ImageMarker

# GIS計算
from geopy import distance

# マップライブラリ
import folium
from folium import LayerControl, plugins

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
    marker_cluster = plugins.MarkerCluster(name="写真").add_to(map)

    for index, marker in enumerate(image_markers, 0):
        file_name = marker.file_path.name
        file_path = marker.file_path.as_posix()
        print(file_path)
        # ポップアップの作成(「show=True」で常に表示)
        exif_info = "<br>".join(
            [f"{key}: {value}" for key, value in marker.exif_image.exif.items()])

        p_up = folium.Popup(
            html=f"<center>{index}: {file_name}</center><br><div style='display: flex'><div><img width='90%' src='{file_path}'></div><div>{exif_info}</div></div>",
            min_width=0,
            max_width=500,
            show=True)

        # 地図オブジェクトにプロット
        folium.Marker(
            location=marker.location,
            popup=p_up).add_to(marker_cluster)

    # 円の範囲内計算
    # https://teratail.com/questions/281188
    redius = 100
    p_up = folium.Popup(
        html=f"redius: {redius}",
        show=True
    )
    folium.Circle(
        location=image_markers[0].location,
        radius=redius,
        popup=p_up,
        color='#3186cc',
        fill_color='#3186cc').add_to(map)

    # 距離計算
    dist = distance.distance(
        image_markers[0].location,
        image_markers[1].location)
    print(f"dist: {dist}")

    # レイヤーを切り替えられる
    LayerControl().add_to(map)
    # 地図表示
    map.save('index.html')

    webbrowser.open("index.html")


def marker_help():
    help(plugins.MarkerCluster)

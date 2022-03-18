from exif_photo.ImageMarker import ImageMarker

# ファイル操作
from pathlib import Path

# マップライブラリ
import folium
from folium import LayerControl, plugins

# GIS計算
from geopy import distance

import webbrowser


def search_file(search_dir: str, pattern: str) -> list[Path]:
    path = Path(search_dir)
    filepaths: list[Path] = list(path.glob(pattern))
    if not filepaths:
        print(f"{search_dir}は画像ファイルが存在しません。")
        # TODO: エラー
        return []

    return filepaths


if __name__ == "__main__":

    def _main():
        filepaths = search_file("./images/", "**/*.png")
        filepaths.extend(search_file("./images/", "**/*.jpg"))

        if not filepaths:
            print("画像ファイルが見つかりませんでした。")
            return

        # 画像ファイルのマーカーオブジェクトの作成

        image_markers: list[ImageMarker] = [
            ImageMarker(path) for path in filepaths]

        print()

        # マップ作成
        map = folium.Map(
            location=image_markers[0].location,
            zoom_start=20)

        # マーカークラスターのレイヤーを作成
        marker_cluster = plugins.MarkerCluster(name="写真").add_to(map)

        for index, marker in enumerate(image_markers, 0):
            file_name = marker.filepath.name
            file_path = marker.filepath.as_posix()
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

        print("finish")

    def marker_help():
        help(plugins.MarkerCluster)

    _main()

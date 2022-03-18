from exif_reader import exif_reader as ERead
from Marker import Marker

# ファイル操作
from pathlib import Path

import webbrowser

import folium
from folium import plugins


if __name__ == "__main__":
    def search_file(search_dir: str, pattern: str) -> list[Path]:
        path = Path(search_dir)
        filepaths: list[Path] = list(path.glob(pattern))
        if not filepaths:
            print(f"{search_dir}は画像ファイルが存在しません。")
            return []

        return filepaths

    def _main():
        filepaths = search_file("./images/", "**/*.png")
        filepaths.extend(search_file("./images/", "**/*.jpg"))

        if not filepaths:
            print("画像ファイルが見つかりませんでした。")
            return

        markers: list[Marker] = []

        for path in filepaths:
            exif_image = ERead.ExifImage(path)
            exif_image.print()
            exif_image.print_geo()

            location = exif_image.get_geo_deg()
            if location is None:
                continue

            marker = Marker(path, location)
            markers.append(marker)

        print()

        map = folium.Map(
            location=markers[0].location,
            zoom_start=20)

        marker_cluster = plugins.MarkerCluster().add_to(map)

        for marker in markers:
            file_name = marker.filepath.as_posix().split("\\")[-1]
            # filepath = marker.filepath
            print(marker.filepath.as_posix())
            # ポップアップの作成(「show=True」で常に表示)
            p_up = folium.Popup(
                html=f"<center>{file_name}<br><img width='100%' src='{marker.filepath.as_posix()}'></center>",
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

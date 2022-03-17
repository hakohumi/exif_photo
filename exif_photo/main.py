from exif_reader import exif_reader as ERead
from Marker import Marker

import glob

import folium

if __name__ == "__main__":
    def search_file(search_dir: str) -> list[str]:
        filepaths = glob.glob(search_dir)
        if not filepaths:
            print(f"{search_dir}は画像ファイルが存在しません。")
            return []
        return filepaths

    def _main():
        filepaths = search_file("./images/**/*.png")
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

        map = folium.Map(
            location=markers[0].location,
            zoom_start=20)

        print()

        for marker in markers:
            filepath = marker.filepath[-10:-1]
            print(filepath)
            # ポップアップの作成(「show=True」で常に表示)
            p_up = folium.Popup(
                filepath,
                min_width=0,
                max_width=1000,
                show=True)

            # 地図オブジェクトにプロット
            folium.Marker(
                location=marker.location,
                popup=p_up).add_to(map)

        # 地図表示
        map.save('index.html')

        print("finish")

    _main()

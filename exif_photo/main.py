from exif_reader import exif_reader as ERead

import glob

import folium

if __name__ == "__main__":
    def _main():
        exif_image = ERead.ExifImage("image.jpg")
        exif_image.print()
        exif_image.print_geo()
        location = exif_image.get_geo_deg()

        map = folium.Map(
            location=location,
            zoom_start=20)

        # ポップアップの作成(「show=True」で常に表示)
        p_up = folium.Popup('写真のジオタグ', min_width=0, max_width=1000, show=True)

        # 地図オブジェクトにプロット
        folium.Marker(
            location=location,
            popup=p_up).add_to(map)

        # 地図表示
        map.save('index.html')

    _main()

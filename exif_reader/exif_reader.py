from typing import Any
from PIL import Image, ExifTags


class ExifImage:
    def __init__(self, file_name):
        self.file_name: str = file_name
        # 画像ファイルを開く --- (*1)
        self.img = Image.open(file_name)
        self.exif: dict[int | str, Any] = {}

        if (self.img.getexif()):
            exif = self.img.getexif()
            for key, value in self.img.getexif().items():
                if ("GPSInfo" == ExifTags.TAGS.get(key, key)):
                    gps_info: dict[int, Any] = exif.get_ifd(key)

                    self.exif["GPSInfo"] = {
                        ExifTags.GPSTAGS.get(key, key): value
                        for key, value in gps_info.items()
                    }
                else:
                    self.exif |= {ExifTags.TAGS.get(key, key): value}

    def print_exif(self):
        if self.exif:
            for k, v in self.exif.items():
                print(k, ":", v)
        else:
            print("exif情報は記録されていません。")

    def print_geo(self):
        if self.exif.get("GPSInfo", None) is None:
            print("GPSInfoがありません。")
            return

        gps = self.exif["GPSInfo"]
        lat = getpos(gps["GPSLatitudeRef"], gps["GPSLatitude"])
        lon = getpos(gps["GPSLongitudeRef"], gps["GPSLongitude"])

        location = f"{lat} {lon}"

        print(location)

    def get_geo_deg(self) -> tuple[float, float] | None:
        if self.exif.get("GPSInfo", None) is None:
            print("GPSInfoがありません。")
            raise ValueError

        gps = self.exif["GPSInfo"]
        return calc_deg(gps)


def getpos(dr, value):
    d = int(value[0])
    m = int(value[1])
    s = value[2]
    return f"{d}°{m}'" + f'{s}"{dr}'  # 'を含む文字列を""で "を含む文字列を''で囲む


def calc_deg(gps_info: dict) -> tuple[float, float] | None:
    if not("GPSLatitude" in gps_info and
            "GPSLatitudeRef" in gps_info and
            "GPSLongitude" in gps_info and
            "GPSLongitudeRef" in gps_info):
        print("GPSInfo内に緯度経度情報がありません。")
        return None

    lat = gps_info['GPSLatitude']
    lat_ref = gps_info['GPSLatitudeRef']
    # GPS情報から経度に関する情報を取り出す
    lon = gps_info['GPSLongitude']
    lon_ref = gps_info['GPSLongitudeRef']


# 北緯の場合プラス、南緯の場合マイナスを設定
    if lat_ref == 'N':
        lat_sign = 1.0
    elif lat_ref == 'S':
        lat_sign = -1.0
    else:
        return None

# 東経の場合プラス、西経の場合マイナスを設定
    if lon_ref == 'E':
        lon_sign = 1.0
    elif lon_ref == 'W':
        lon_sign = -1.0
    else:
        return None

# 度分秒 を 十進経緯度 に変換する
    lat_ang0 = lat_sign * lat[0] + lat[1] / 60 + lat[2] / 3600
    lon_ang0 = lon_sign * lon[0] + lon[1] / 60 + lon[2] / 3600
# コンマ区切りで１つにまとめる
    return lat_ang0, lon_ang0

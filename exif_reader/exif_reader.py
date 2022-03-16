from PIL import Image, ExifTags


class ExifImage:

    def __init__(self, fname):
        # 画像ファイルを開く --- (*1)
        self.img = Image.open(fname)
        self.exif = {}

        if (self.img.getexif()):
            exif = self.img.getexif()
            for key, value in self.img.getexif().items():
                if ("GPSInfo" == ExifTags.TAGS.get(key, key)):
                    gps_info = exif.get_ifd(key)
                    self.exif["GPSInfo"] = {
                        ExifTags.GPSTAGS.get(key, key): value
                        for key, value in gps_info.items()
                    }
                else:
                    self.exif |= {ExifTags.TAGS.get(key, key): value}

    def print(self):
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


def getpos(dr, value):
    d = int(value[0])
    m = int(value[1])
    s = value[2]
    return f"{d}°{m}'" + f'{s}"{dr}'  # 'を含む文字列を""で "を含む文字列を''で囲む

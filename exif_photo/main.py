from exif_reader import exif_reader as ERead

if __name__ == "__main__":
    def _main():
        exif_image = ERead.ExifImage("image.jpg")
        exif_image.print()
        exif_image.print_geo()

    _main()

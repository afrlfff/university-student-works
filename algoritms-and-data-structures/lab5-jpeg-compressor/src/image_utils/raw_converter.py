from PIL import Image
import numpy as np

# Constants
mode2ind = {
    "L": 0,
    "RGB": 1
}
ind2mode = {value: key for key, value in mode2ind.items()}

# Functions
def jpg_to_raw(path_to_jpg, path_to_raw):
    image = Image.open(path_to_jpg)

    width, height = image.size
    mode = image.mode
    pixels = image.getdata()

    with open(path_to_raw, "wb") as f:
        # write header
        f.write(width.to_bytes(2, byteorder='little'))
        f.write(height.to_bytes(2, byteorder='little'))
        f.write(mode2ind[mode].to_bytes(1, byteorder='little'))

        # write pixels
        if mode == "L":
            for pixel in pixels:
                f.write(pixel.to_bytes(1, byteorder='little'))
        elif mode == "RGB":
            for pixel in pixels:
                f.write(pixel[0].to_bytes(1, byteorder='little'))
                f.write(pixel[1].to_bytes(1, byteorder='little'))
                f.write(pixel[2].to_bytes(1, byteorder='little'))
        else:
            raise ValueError("Unknown image mode.")

def raw_to_jpg(path_to_raw, path_to_jpg):
    with open(path_to_raw, "rb") as f:
        width = int.from_bytes(f.read(2), byteorder='little')
        height = int.from_bytes(f.read(2), byteorder='little')
        mode = ind2mode[int.from_bytes(f.read(1), byteorder='little')]

        pixels = []
        if mode == "L":
            for _ in range(height):
                row_pixels = []
                for __ in range(width):
                    row_pixels.append(int.from_bytes(f.read(1), byteorder='little'))
                pixels.append(row_pixels)
        elif mode == "RGB":
            for _ in range(height):
                row_pixels = []
                for __ in range(width):
                    row_pixels.append([int.from_bytes(f.read(1), byteorder='little'),
                                      int.from_bytes(f.read(1), byteorder='little'),
                                      int.from_bytes(f.read(1), byteorder='little')])
                pixels.append(row_pixels)
        else:
            raise ValueError("Unknown image mode.")

        img = Image.fromarray(np.array(pixels).astype(np.uint8), mode)
        img.save(path_to_jpg)

def raw_to_img(path_to_raw):
    with open(path_to_raw, "rb") as f:
        width = int.from_bytes(f.read(2), byteorder='little')
        height = int.from_bytes(f.read(2), byteorder='little')
        mode = ind2mode[int.from_bytes(f.read(1), byteorder='little')]

        pixels = []
        if mode == "L":
            for _ in range(height):
                row_pixels = []
                for __ in range(width):
                    row_pixels.append(int.from_bytes(f.read(1), byteorder='little'))
                pixels.append(row_pixels)
        elif mode == "RGB":
            for _ in range(height):
                row_pixels = []
                for __ in range(width):
                    row_pixels.append([int.from_bytes(f.read(1), byteorder='little'),
                                      int.from_bytes(f.read(1), byteorder='little'),
                                      int.from_bytes(f.read(1), byteorder='little')])
                pixels.append(row_pixels)
        else:
            raise ValueError("Unknown image mode.")

        return Image.fromarray(np.array(pixels).astype(np.uint8), mode)
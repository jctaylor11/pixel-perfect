import sys
from PIL import Image

# Alpha above a threshold filters out invisible pixels (assumes transparent background)
ALPHA_THRESHOLD = 10


def row_has_content(pixels, y, width):
    for x in range(width):
        if pixels[x, y][3] > ALPHA_THRESHOLD:
            return True
    return False


def col_has_content(pixels, x, height):
    for y in range(height):
        if pixels[x, y][3] > ALPHA_THRESHOLD:
            return True
    return False


def find_bounds(img):
    pixels = img.load()
    width, height = img.size

    top = None
    for y in range(height):
        if row_has_content(pixels, y, width):
            top = y
            break

    bottom = None
    for y in range(height - 1, -1, -1):
        if row_has_content(pixels, y, width):
            bottom = y
            break

    left = None
    for x in range(width):
        if col_has_content(pixels, x, height):
            left = x
            break

    right = None
    for x in range(width - 1, -1, -1):
        if col_has_content(pixels, x, height):
            right = x
            break

    if None in (top, bottom, left, right):
        raise ValueError("No visible content found in image")

    return (left, top, right, bottom)


def print_bounds(bounds):
    left, top, right, bottom = bounds
    w = right - left + 1
    h = bottom - top + 1
    print(f"bounds: left={left} top={top} right={right} bottom={bottom} ({w}x{h})")


def main(path):
    img = Image.open(path).convert("RGBA")
    bounds = find_bounds(img)
    print_bounds(bounds)
    

if __name__ == "__main__":
    main(sys.argv[1])

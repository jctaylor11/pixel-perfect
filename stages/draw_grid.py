from PIL import Image, ImageDraw


def grid_draw(input_img, block_size):
    GRID_RGBA = (0, 255, 0, 120)

    img = input_img.convert("RGBA")     # To ensure it's mode matches grid_overlay's

    grid_overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))     # Starting with fully transparent overlay
    draw = ImageDraw.Draw(grid_overlay)

    width, height = img.size
    for x in range(0, width, block_size):
        draw.line(([x, 0], [x, height]), fill=GRID_RGBA, width=1)
    for y in range(0, height, block_size):
        draw.line(([0, y], [width, y]), fill=GRID_RGBA, width=1)

    img_with_grid = Image.alpha_composite(img, grid_overlay)

    return img_with_grid

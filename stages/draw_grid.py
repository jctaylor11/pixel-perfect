from PIL import Image, ImageDraw


def grid_draw(input_img, block_size, grid_rgba=(0, 255, 0, 120)):
    img = input_img.convert("RGBA")     # To ensure it's mode matches grid_overlay's

    grid_overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))     # Starting with fully transparent overlay
    draw = ImageDraw.Draw(grid_overlay)

    width, height = img.size
    for x in range(0, width + 1, block_size):
        x = min(x, width - 1)   # Closing line on the last pixel when width is a whole number of blocks
        draw.line([(x, 0), (x, height)], fill=grid_rgba, width=1)
    for y in range(0, height + 1, block_size):
        y = min(y, height - 1)
        draw.line([(0, y), (width, y)], fill=grid_rgba, width=1)

    img_with_grid = Image.alpha_composite(img, grid_overlay)

    return img_with_grid

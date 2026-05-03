from PIL import Image, ImageDraw


def grid_draw(input_path, block_size, output_path):
    GRID_RGBA = (255, 0, 0, 120)

    img = Image.open(input_path)
    img = img.convert("RGBA")     # To ensure it's mode matches grid_overlay's

    grid_overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))     # Starting with fully transparent overlay
    draw = ImageDraw.Draw(grid_overlay)

    width, height = img.size
    for x in range(0, width, block_size):
        draw.line(([x, 0], [x, height]), fill=GRID_RGBA, width=1)
    for y in range(0, height, block_size):
        draw.line(([0, y], [width, y]), fill=GRID_RGBA, width=1)

    # Overlaying grid for visual assessment for now
    img_with_grid = Image.alpha_composite(img, grid_overlay)
    img_with_grid.save(output_path)
    print(f"Image with grid saved to {output_path}")


if __name__ == "__main__":
    # For testing
    INPUT_PATH = 'inputs/sprite_cropped.png'
    BLOCK_SIZE = 13
    OUTPUT_PATH = 'outputs/grid_output.png'

    grid_draw(INPUT_PATH, BLOCK_SIZE, OUTPUT_PATH)

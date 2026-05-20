from PIL import Image
import numpy as np
import math


def construct_blocks(block_colours, block_size, cropped_shape):
    """Reconstruct cropped image with quantised colours.
    """
    img_height, img_width = cropped_shape
    blocks_rows = math.ceil(img_height / block_size)
    blocks_cols = math.ceil(img_width / block_size)

    block_grid = block_colours.reshape(blocks_rows, blocks_cols, 4)
    output_pixels = np.zeros((blocks_rows * block_size, blocks_cols * block_size, 4), dtype=np.uint8)

    for block_row in range(blocks_rows):
        for block_col in range(blocks_cols):
            y_start = block_row * block_size
            x_start = block_col * block_size
            output_pixels[y_start:y_start+block_size, x_start:x_start+block_size] = block_grid[block_row, block_col]

    reconstructed_img = Image.fromarray(output_pixels)

    return reconstructed_img

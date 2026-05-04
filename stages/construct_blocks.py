from PIL import Image
import numpy as np

from stages.sample_blocks import sample_blocks
from stages.draw_grid import grid_draw


def construct_blocks(block_array, block_size, output_path):
    blocks_rows, blocks_cols, _ = block_array.shape

    reconstruction = np.zeros((blocks_rows * block_size, blocks_cols * block_size, 4), dtype=np.uint8)

    for row in range(0, blocks_rows):
        for col in range(0, blocks_cols):
            pixel_row = row * block_size
            pixel_col = col * block_size
            reconstruction[pixel_row:pixel_row+block_size, pixel_col:pixel_col+block_size, :] = block_array[row][col]

    reconstructed = Image.fromarray(reconstruction)
    reconstructed.save(output_path)

    grid_output_path = output_path[:-4] + "_grid.png"
    grid_draw(output_path, block_size, grid_output_path)
            

    

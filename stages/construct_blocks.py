from PIL import Image
import numpy as np


def construct_blocks(block_array, block_size):
    blocks_rows, blocks_cols, _ = block_array.shape

    reconstruction = np.zeros((blocks_rows * block_size, blocks_cols * block_size, 4), dtype=np.uint8)

    for row in range(0, blocks_rows):
        for col in range(0, blocks_cols):
            pixel_row = row * block_size
            pixel_col = col * block_size
            reconstruction[pixel_row:pixel_row+block_size, pixel_col:pixel_col+block_size, :] = block_array[row][col]

    reconstructed_img = Image.fromarray(reconstruction)
    
    return reconstructed_img

            

    

import numpy as np 
from PIL import Image
from collections import Counter
import math


def sample_blocks(input_img, block_size): 
    img = input_img.convert('RGBA')

    img_arr = np.array(img)
    height, width, _ = img_arr.shape

    num_blocks_height = math.ceil(height / block_size)
    num_blocks_width = math.ceil(width / block_size)

    new_blocks = np.zeros((num_blocks_height, num_blocks_width, 4), dtype=np.uint8)
    
    for row_index, row_pixel in enumerate(range(0, height, block_size)):
        for col_index, col_pixel in enumerate(range(0, width, block_size)):
            # Each block being sampled is square
            sample = img_arr[row_pixel:row_pixel+block_size, col_pixel:col_pixel+block_size] 

            # Reshape from 3D array to 2D to make count comparisons
            pixel_lists = sample.reshape(-1, 4)

            # Pixel array needs to be a tuple to run counts (hashable)
            pixel_tuples = map(tuple, pixel_lists)
            
            most_common_pixel, freq = Counter(pixel_tuples).most_common(1)[0]

            # 3D array represents the colour for each block of size block_size
            new_blocks[row_index][col_index] = most_common_pixel

    return new_blocks


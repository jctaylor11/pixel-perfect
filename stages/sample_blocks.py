import numpy as np
from collections import Counter
import math


def sample_center(block):
    height, width, _ = block.shape
    return tuple(block[height // 2, width // 2])


def sample_most_common(block):
    pixel_tuples = map(tuple, block.reshape(-1, 4))
    most_common, _ = Counter(pixel_tuples).most_common(1)[0]
    return most_common


def sample_most_common_bucketed(block, bucket_size=16):
    bucketed = (block // bucket_size) * bucket_size     
    pixel_tuples = map(tuple, bucketed.reshape(-1, 4))
    most_common, _ = Counter(pixel_tuples).most_common(1)[0]
    return most_common


def sample_inner_weighted(block):
    height, width, _ = block.shape
    row_trim = max(1, int(height * 0.2))
    col_trim = max(1, int(width * 0.2))
    inner = block[row_trim:height - row_trim, col_trim:width - col_trim]
    if inner.size == 0:
        inner = block

    counts = Counter(map(tuple, inner.reshape(-1, 4)))
    total_weight = 0
    weighted_sum = np.zeros(4, dtype=np.float64)
    for colour, count in counts.items():
        weight = count * count
        weighted_sum += weight * np.array(colour, dtype=np.float64)
        total_weight += weight

    return tuple((weighted_sum / total_weight).round().astype(np.uint8))


def sample_blocks(cropped_img, block_size, sampler=sample_inner_weighted):
    img = cropped_img.convert('RGBA')

    img_arr = np.array(img)
    height, width, _ = img_arr.shape

    num_blocks_height = math.ceil(height / block_size)
    num_blocks_width = math.ceil(width / block_size)

    new_blocks = np.zeros((num_blocks_height, num_blocks_width, 4), dtype=np.uint8)

    for row_index, row_pixel in enumerate(range(0, height, block_size)):
        for col_index, col_pixel in enumerate(range(0, width, block_size)):
            block = img_arr[row_pixel:row_pixel+block_size, col_pixel:col_pixel+block_size]
            new_blocks[row_index][col_index] = sampler(block)

    return new_blocks

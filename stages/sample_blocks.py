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


def sample_palette_proximity(block, bucket_size=16):
    height, width, _ = block.shape
    row_trim = max(1, int(height * 0.2))
    col_trim = max(1, int(width * 0.2))
    inner = block[row_trim:height - row_trim, col_trim:width - col_trim]
    if inner.size == 0:
        inner = block

    pixels = inner.reshape(-1, 4).astype(np.float64)
    centroids = (pixels // bucket_size) * bucket_size

    best_score = -1
    best_centroid = None
    for centroid in np.unique(centroids, axis=0):
        mask = np.all(centroids == centroid, axis=1)
        count = mask.sum()
        mean_distance = np.linalg.norm(pixels[mask] - centroid, axis=1).mean()
        score = (count ** 2) / (mean_distance + 1)
        if score > best_score:
            best_score = score
            best_centroid = centroid

    distances_to_best = np.linalg.norm(pixels - best_centroid, axis=1)
    return tuple(pixels[np.argmin(distances_to_best)].round().astype(np.uint8))


def sample_blocks(cropped_img, block_size, sampler=sample_center):
    """Downsample an upscaled sprite to its logical pixel grid.

    Divides the image into a grid of block_size × block_size patches and
    reduces each patch to a single RGBA colour via the sampler. The result
    is the sprite at its native resolution: one output pixel per sprite block.

    Args: 
        cropped_img: PIL Image cropped to sprite bounds
        block_size: number of pixels per sprite block
        sampler: function that determines each block's colours

    Returns:
        NDArray[np.uint8] of shape (num_blocks, 4)
        
        Each row is one sprite block's RGBA colour. 
        Reshaping to (ceil(height / block_size), ceil(width / block_size), 4) recovers the 2D logical sprite.
    """
    rgba_img = cropped_img.convert('RGBA')

    pixel_arr = np.array(rgba_img)
    height, width, _ = pixel_arr.shape

    block_rows = math.ceil(height / block_size)
    block_cols = math.ceil(width / block_size)

    block_grid = np.zeros((block_rows, block_cols, 4), dtype=np.uint8)

    for block_row, y_start in enumerate(range(0, height, block_size)):
        for block_col, x_start in enumerate(range(0, width, block_size)):
            block_pixels = pixel_arr[y_start:y_start+block_size, x_start:x_start+block_size]
            block_grid[block_row, block_col] = sampler(block_pixels)

    flattened_blocks = block_grid.reshape(-1, 4)    # Array of sampled colours, one pixel RGBA per sprite block

    return flattened_blocks

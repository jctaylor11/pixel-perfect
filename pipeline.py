from PIL import Image

from stages.find_bounds import find_bounds, crop_image
from stages.sample_blocks import sample_blocks
from stages.construct_blocks import construct_blocks
from config import INPUT_PATH, CROPPED_PATH, OUTPUT_PATH, BLOCK_SIZE


def pipeline(input_path, cropped_path, output_path, block_size):
    img = Image.open(input_path)
    img = img.convert('RGBA')

    image_bounds = find_bounds(img)
    cropped_path = crop_image(img, image_bounds, cropped_path)

    new_blocks_array = sample_blocks(cropped_path, block_size)

    construct_blocks(new_blocks_array, block_size, output_path)


if __name__ == "__main__":
    pipeline(INPUT_PATH, CROPPED_PATH, OUTPUT_PATH, BLOCK_SIZE)

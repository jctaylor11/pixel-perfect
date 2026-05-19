from PIL import Image
import argparse

from stages.find_bounds import find_bounds, crop_image
from stages.sample_blocks import sample_blocks
from stages.quantise_colours import quantise_colours
from stages.construct_blocks import construct_blocks
from stages.place_on_canvas import place_on_canvas
from stages.save_outputs import save_outputs
import config

def pipeline(input_path, block_size, n_colours, padding):
    img = Image.open(input_path)
    img = img.convert('RGBA')

    image_bounds = find_bounds(img)
    cropped_img = crop_image(img, image_bounds)

    blocks_array = sample_blocks(cropped_img, block_size)
    quantized_blocks = quantise_colours(blocks_array, n_colours)
    reconstructed_img = construct_blocks(quantized_blocks, block_size)
    canvas_img = place_on_canvas(reconstructed_img, padding)

    save_outputs(input_path, cropped_img, block_size, reconstructed_img, canvas_img)



if __name__ == "__main__":
    # CLI args make it easy to compare changes between block sizes without going back into the config file
    parser = argparse.ArgumentParser()
    parser.add_argument("--block_size", type=int, default=config.BLOCK_SIZE)
    parser.add_argument("--input_path", type=str, default=config.INPUT_PATH)
    parser.add_argument("--n_colours", type=int, default=config.N_COLOURS)
    parser.add_argument("--padding", type=int, default=config.PADDING)
    args = parser.parse_args()

    INPUT_PATH = args.input_path
    BLOCK_SIZE = args.block_size
    N_COLOURS = args.n_colours
    PADDING = args.padding

    pipeline(INPUT_PATH, BLOCK_SIZE, N_COLOURS, PADDING)

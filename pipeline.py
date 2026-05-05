from PIL import Image
import argparse

from stages.find_bounds import find_bounds, crop_image
from stages.sample_blocks import sample_blocks
from stages.construct_blocks import construct_blocks
from stages.draw_grid import grid_draw
import config

def pipeline(input_file, block_size):
    input_path = './inputs/' + input_file

    img = Image.open(input_path)
    img = img.convert('RGBA')

    image_bounds = find_bounds(img)
    cropped_img = crop_image(img, image_bounds)

    new_blocks_array = sample_blocks(cropped_img, block_size)

    reconstructed_img = construct_blocks(new_blocks_array, block_size)

    ## Outputs ## 

    # Original image cropped
    cropped_path = "./outputs/" + "cropped_" + input_file
    cropped_img.save(cropped_path)

    # Original image cropped with grid
    cropped_grid_path = "./outputs/" + "grid_" + input_file
    cropped_with_grid = grid_draw(cropped_img, block_size)
    cropped_with_grid.save(cropped_grid_path)
    
    # Reconstructed image
    final_image_path = './outputs/' + "reconstructed_" + input_file
    reconstructed_img.save(final_image_path)

    # Reconstructed image with grid
    final_grid_path = './outputs/' + "reconstructed_grid_" + input_file
    reconstructed_with_grid = grid_draw(reconstructed_img, block_size)
    reconstructed_with_grid.save(final_grid_path)




if __name__ == "__main__":
    # CLI args make it easy to compare changes between block sizes without going back into the config file
    parser = argparse.ArgumentParser()
    parser.add_argument("--block_size", type=int, default=config.BLOCK_SIZE)
    parser.add_argument("--input_file", type=str, default=config.INPUT_FILE)
    args = parser.parse_args()

    INPUT_FILE = args.input_file
    BLOCK_SIZE = args.block_size

    pipeline(INPUT_FILE, BLOCK_SIZE)

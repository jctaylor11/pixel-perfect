import argparse
import os

from dotenv import load_dotenv
from PIL import Image
from pydantic import BaseModel
import numpy as np
from numpy.typing import NDArray


load_dotenv()

from stages.find_bounds import find_bounds, crop_image
from stages.sample_blocks import sample_blocks
from stages.quantise_colours import compute_centroids, quantise_to_centroids
from stages.construct_blocks import construct_blocks
from stages.place_on_canvas import place_on_canvas
from stages.save_outputs import save_clean_output, save_debug_outputs
from stages.watermark_image import add_watermark
import config

class SpriteImage(BaseModel):
    block_colours: NDArray[np.uint8]
    cropped_img_shape: tuple[int, int]
    input_filepath: str

    model_config = {"arbitrary_types_allowed": True}


def pipeline_folder(folder_path, block_size, num_colours, padding):
    sprite_dict = {}

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        filepath = os.path.join(folder_path, filename)
        img_raw = Image.open(filepath)
        img_rgba = img_raw.convert('RGBA')
        img_bounds = find_bounds(img_rgba)

        cropped_img = crop_image(img_rgba, img_bounds)
        block_colours = sample_blocks(cropped_img, block_size)
        cropped_img_shape = (cropped_img.height, cropped_img.width)     # PIL and Numpy use inverses for shape/size, so shape is manually set for numpy convention

        sprite = SpriteImage(
            block_colours=block_colours,
            cropped_img_shape=cropped_img_shape,
            input_filepath=filepath,
        )

        sprite_dict[filename] = sprite

    # Combine arrays, find centroids, reconstruct individual arrays, quantise blocks with found centroids
    combined_block_colours = np.concatenate([sprite.block_colours.reshape(-1,4) for sprite in sprite_dict.values()])
    centroids = compute_centroids(combined_block_colours, num_colours)
    
    for filename, sprite in sprite_dict.items():
        quantised_blocks = quantise_to_centroids(sprite.block_colours, centroids)
        reconstructed_img = construct_blocks(quantised_blocks, block_size, sprite.cropped_img_shape)
        canvas_img = place_on_canvas(reconstructed_img, padding)
        watermarked_img = add_watermark(canvas_img)

        output_filepath = sprite.input_filepath.replace('inputs', 'outputs')
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        watermarked_img.save(output_filepath)


def pipeline_folder_individual(folder_path, block_size, num_colours, padding):
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        filepath = os.path.join(folder_path, filename)
        pipeline_image(filepath, block_size, num_colours, padding)


def pipeline_image(input_path, block_size, num_colours, padding):
    img_raw = Image.open(input_path)
    img_rgba = img_raw.convert('RGBA')

    image_bounds = find_bounds(img_rgba)
    cropped_img = crop_image(img_rgba, image_bounds)
    cropped_img_shape = (cropped_img.height, cropped_img.width)     # PIL and Numpy use inverses for shape/size, so shape is manually set for numpy convention

    block_colours = sample_blocks(cropped_img, block_size)           # Blocks array is array of sampled colours, one pixel RGBA per sprite block
    centroids = compute_centroids(block_colours, num_colours)
    quantised_blocks = quantise_to_centroids(block_colours, centroids)

    reconstructed_img = construct_blocks(quantised_blocks, block_size, cropped_img_shape)
    canvas_img = place_on_canvas(reconstructed_img, padding)
    watermarked_canvas_img = add_watermark(canvas_img)

    # save_debug_outputs(input_path, cropped_img, block_size, reconstructed_img, watermarked_canvas_img)
    save_clean_output(input_path, watermarked_canvas_img)


if __name__ == "__main__":
    # CLI args make it easy to compare changes between block sizes without going back into the config file
    parser = argparse.ArgumentParser()
    parser.add_argument("--block_size", type=int, default=config.BLOCK_SIZE)
    parser.add_argument("--input_image", type=str, default=config.INPUT_IMAGE_PATH)
    parser.add_argument("--folder", type=str, default=config.INPUT_FOLDER_NAME)
    parser.add_argument("--num_colours", type=int, default=config.NUM_COLOURS)
    parser.add_argument("--padding", type=int, default=config.PADDING)
    args = parser.parse_args()

    INPUT_IMAGE = args.input_image
    INPUT_FOLDER = f"./inputs/{args.folder}/"
    INDIVIDUAL_INPUTS = "./inputs/individual/"
    BLOCK_SIZE = args.block_size
    NUM_COLOURS = args.num_colours
    PADDING = args.padding

    # pipeline_image(INPUT_IMAGE, BLOCK_SIZE, NUM_COLOURS, PADDING)
    pipeline_folder(INPUT_FOLDER, BLOCK_SIZE, NUM_COLOURS, PADDING)
    pipeline_folder_individual(INDIVIDUAL_INPUTS, BLOCK_SIZE, NUM_COLOURS, PADDING)


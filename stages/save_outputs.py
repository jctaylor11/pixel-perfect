from stages.draw_grid import grid_draw
from pathlib import Path


def build_output_path(input_path, slug):
    input_path = Path(input_path)
    output_path = Path("outputs") / input_path.parent.relative_to("inputs") / (slug + "_" + input_path.name)
    return output_path


def save_outputs(input_path, cropped_img, block_size, reconstructed_img, canvas_img):
    # Original image cropped
    cropped_path = build_output_path(input_path, "cropped")
    cropped_img.save(cropped_path)

    # Original image cropped with grid
    cropped_grid_img = grid_draw(cropped_img, block_size)
    cropped_grid_path = build_output_path(input_path, "grid")
    cropped_grid_img.save(cropped_grid_path)
    
    # Reconstructed image
    reconstructed_img_path = build_output_path(input_path, "reconstructed")
    reconstructed_img.save(reconstructed_img_path)

    # Reconstructed image with grid
    reconstructed_grid_path = build_output_path(input_path, "reconstructed_grid")
    reconstructed_grid_img = grid_draw(reconstructed_img, block_size)
    reconstructed_grid_img.save(reconstructed_grid_path)

    # Canvas
    canvas_path = build_output_path(input_path, "canvas")
    canvas_img.save(canvas_path)
    
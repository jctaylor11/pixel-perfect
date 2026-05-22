from PIL import Image

from config import BACKGROUND_COLOUR


def place_on_canvas(img, padding=100, canvas_size=(1080, 1350)):    # 1080 x 1350 is optimal for Instagram
    canvas_w, canvas_h = canvas_size
    available_w = canvas_w - 2 * padding
    available_h = canvas_h - 2 * padding

    # Integer scale so every sprite block ends up the same number of canvas pixels
    scale = max(1, min(available_w // img.width, available_h // img.height))
    scaled_w = img.width * scale
    scaled_h = img.height * scale
    scaled_img = img.resize((scaled_w, scaled_h), Image.NEAREST)    # Nearest so it doesn't interpolate colours - maintains sharp colour boundaries

    canvas = Image.new("RGBA", canvas_size, BACKGROUND_COLOUR)
    offset_x = (canvas_w - scaled_w) // 2
    offset_y = (canvas_h - scaled_h) // 2
    canvas.paste(scaled_img, (offset_x, offset_y), scaled_img)      # Scaled_img already has transparent background so can be used as mask argument

    return canvas

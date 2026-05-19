import aggdraw
import os
from PIL import ImageDraw, ImageFont

from config import FONT_PATH, FONT_SIZE, FONT_PADDING

watermark_text = os.getenv("WATERMARK_TEXT")


def add_watermark(canvas):
    canvas = canvas.copy()
    padding = FONT_PADDING

    # measure text size using PIL first
    temp_draw = ImageDraw.Draw(canvas)
    pil_font = ImageFont.truetype(FONT_PATH, size=FONT_SIZE)
    bbox = temp_draw.textbbox((0, 0), watermark_text, font=pil_font)  # Returns (left, top, right, bottom)
    text_w = bbox[2] - bbox[0]  # right - left
    text_h = bbox[3] - bbox[1]  # bottom - top

    # Coords for top left corner of text
    x = canvas.width - text_w - (padding / 2)   # /2 as adjusted visually 
    y = canvas.height - text_h - padding

    agg = aggdraw.Draw(canvas)  # aggdraw produces higher quality text rendering than PIL

    # For embossed effect - layer highlight, shadow, and main with small offsets
    highlight_font = aggdraw.Font((255, 255, 255, 100), FONT_PATH, size=FONT_SIZE)
    shadow_font = aggdraw.Font((0, 0, 0, 100), FONT_PATH, size=FONT_SIZE)
    main_font = aggdraw.Font((180, 180, 180, 255), FONT_PATH, size=FONT_SIZE)

    agg.text((x - 1, y - 1), watermark_text, highlight_font)
    agg.text((x + 1, y + 1), watermark_text, shadow_font)
    agg.text((x, y), watermark_text, main_font)

    agg.flush()

    return canvas

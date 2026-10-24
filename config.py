
INPUT_FOLDER_NAME = "astro_cat"
INPUT_IMAGE_PATH = "./inputs/orange_hoodie/front.png"     # Must be in inputs/ folder

BLOCK_SIZE = 13
ALPHA_THRESHOLD = 10    # Needed to filter out invisible pixels
NUM_COLOURS = 8         # For quantisation
PADDING = 100
BACKGROUND_COLOUR = "#c7b299"
COMPARISON_GRID_RGBA = (255, 0, 255, 160)   # Magenta stands out on green sprites, unlike the debug grid's green

WATERMARK_TEXT = "pixel-perfect"      # For text on bottom right corner
FONT_PATH = "fonts/Outfit-VariableFont_wght.ttf"
FONT_SIZE = 40
FONT_PADDING = 20


# Testing background colours
#b8d4c8 - dusty blue
#c7b299 - dusty latte
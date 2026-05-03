# pixel-grid-pipeline

## Process
1 - `find_bounds.py`. Finds image bounds assuming transparent padding. Outputs the box coordinates (top, bottom, left, right) of the pixel art content and cropped image. Ensures the pixel analysis starts from content edge.

2 - `draw_grid.py`. Takes the cropped output from `find_bounds.py` and a block size. Outputs the image overlayed with a grid of the given size. Used as a manual stage for visual analysis before alignment of blocks with effective pixels is automated.

3 - `sample_blocks.py`. Takes the image and block size. Loops through each block in the image and samples the most common pixel RGBA. Outputs a 3D array representing each block colours of the final reconstruction.
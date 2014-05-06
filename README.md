Isometric map renderer for Python

Takes an N x M map of RGBA values and pixel height values and represents them as a NxM isometric block.

The input color_grid a numpy array size N x M x 4, where N is the desired height, M is width, and the 4 represents the RGBA values (integers 0-255 or uint8).

The input height_grid is a N x M x 1 numpy array N x M and a positive integer pixel height, representing how tall each corresponding block will be.

Make sure image_assets contains the top, middle, and bottom .pngs.

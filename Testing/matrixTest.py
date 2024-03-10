#! /usr/bin/env python3
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'# Important don't forget

matrix = RGBMatrix(options = options)

offset_canvas = matrix.CreateFrameCanvas()

for y in range(32):
    for x in range(32):
        offset_canvas.SetPixel(x, y, 255, 0, 0)
        offset_canvas = matrix.SwapOnVSync(offset_canvas)

# Run with sudo python3 matrixTest.py

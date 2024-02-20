#!/usr/bin/env python
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'# Important don't forget

matrix = RGBMatrix(options = options)

for y in range(32):
    for x in range(32):
        matrix.SetPixel(x, y, 255, 0, 0)
        matrix.SwapOnVsync()

# Run with sudo ./importTest.py after chmod +x importTest.py
# chmod should not modify the file in any way tho

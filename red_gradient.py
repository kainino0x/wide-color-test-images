#!/usr/bin/env python3

# Dependencies:
#   python3 -m pip install numpy pypng
import numpy
import png
import subprocess
import sys


def make_png(outfile, *, width, height, bits, grad_stride, icc=''):
    """
    Generates a horizontal red gradient, starting from 0 and increasing by 1 "ULP" at a time.
    - height, width: size of resulting image in pixels
    - bits: number of bits in the output image
    - grad_stride: x pixels between increments of the gradient
    - icc: path to icc profile to reinterpret into
    """

    if bits <= 8:
        dtype = numpy.uint8
    elif bits <= 16:
        dtype = numpy.uint16
    else:
        assert False

    data = numpy.zeros((height, width * 3), dtype=dtype)
    for x in range(width):
        red = x // grad_stride
        for y in range(height):
            data[y, x * 3 + 0] = red

    print(data)
    result = png.from_array(data, mode='RGB;{}'.format(bits))
    result.save('tmp.png')

    # Add the ICC profile and stuff
    subprocess.run(['sh', 'step2.sh', outfile, 'tmp.png', icc])

    # Verify the final result contains the correct data
    with open(outfile, 'rb') as f:
        readback = png.Reader(file=f)
        readback_data = numpy.vstack(
            list(map(numpy.uint16, readback.asDirect()[2])))
    print('readback equals original?', numpy.array_equal(data, readback_data))


# RGB, 10-bit (0-1023 range)
make_png('red_gradient_10bit_untagged.png',
         width=256, height=16, bits=10, grad_stride=4)
make_png('red_gradient_10bit_aces.png',
         width=256, height=16, bits=10, grad_stride=4,
         icc='elles_icc_profiles/profiles/ACES-elle-V4-g10.icc')
# RGB, 8-bit (0-255 range)
make_png('red_gradient_8bit_untagged.png',
         width=256, height=16, bits=8, grad_stride=16)
make_png('red_gradient_8bit_aces.png',
         width=256, height=16, bits=8, grad_stride=16,
         icc='elles_icc_profiles/profiles/ACES-elle-V4-g10.icc')

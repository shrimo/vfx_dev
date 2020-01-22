# Read position from OpenEXR

import OpenEXR
import amg_imath
import numpy


def read_exr(filename):
    pt = amg_imath.PixelType(amg_imath.PixelType.FLOAT)
    exr_file = OpenEXR.InputFile(filename)
    dw = exr_file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    # read RGB channel
    channel = 'RGB'
    position_str = {}
    position = {}
    for c in channel:
        position_str[c] = exr_file.channel(c, pt)
        position[c] = numpy.fromstring(position_str[c], dtype=numpy.float32)
        position[c].shape = (size[1], size[0])  # Numpy arrays are (row, col)
    
    print position['R'][270, 243]
        
    


exr_file = '//home/v.lavrentev/project/class/vfx_dev/openexr/position.exr'
read_exr(exr_file)

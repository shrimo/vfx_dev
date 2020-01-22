# Read position from OpenEXR

import OpenEXR
import amg_imath
import array


def read_exr(filename):
    pt = amg_imath.PixelType(amg_imath.PixelType.FLOAT)
    exr_file = OpenEXR.InputFile(filename)
    dw = exr_file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    # read RGB channel
    pos_x = []
    pos_y = []
    pos_z = []
    for c in 'RGB':
        position_str = exr_file.channel(c, pt)
        position = array.array('f', position_str).tolist()
        for pos in position:
            if pos != 0.0:
                if c == 'R':
                    pos_x.append(pos)
                if c == 'G':
                    pos_y.append(pos)
                if c == 'B':
                    pos_z.append(pos)


exr_file = '//home/v.lavrentev/project/class/vfx_dev/openexr/position.exr'
read_exr(exr_file)

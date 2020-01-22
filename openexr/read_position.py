# Read position from OpenEXR

import OpenEXR
import amg_imath
import array


def read_exr(filename):
    # read RGB channel
    pt = amg_imath.PixelType(amg_imath.PixelType.FLOAT)
    exr_file = OpenEXR.InputFile(filename)
    all_pos = []
    for c in 'RGB':
        position_str = exr_file.channel(c, pt)
        position = array.array('f', position_str).tolist()
        pos = []
        for p in position:
            if p != 0.0:
                pos.append(p)
        all_pos.append(pos)    

    return all_pos


exr_file = '//home/v.lavrentev/project/class/vfx_dev/openexr/position.exr'
P = read_exr(exr_file)

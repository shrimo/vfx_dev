# Create object by position

import OpenEXR
import amg_imath
import array
import maya.cmds as cmds


def read_exr(filename, group_name, shape_name):
    pt = amg_imath.PixelType(amg_imath.PixelType.FLOAT)
    exr_file = OpenEXR.InputFile(filename)
    dw = exr_file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    cmds.group(em=True, name=group_name)

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
                    pos_x.append(pos * 10)
                if c == 'G':
                    pos_y.append(pos * 10)
                if c == 'B':
                    pos_z.append(pos * 10)

    # create object
    for i in range(len(pos_x)):
        p_name = shape_name + '_' + str(i)
        cmds.polyCube(n=p_name)  # create polyCube name by p_ + i
        cmds.setAttr(p_name + '.translate', pos_x[i], pos_y[i], pos_z[i])
        cmds.group(p_name, parent=group_name)


def start():
    exr_file = '//home/v.lavrentev/project/class/vfx_dev/openexr/position.exr'
    read_exr(exr_file, 'boxes', 'sphere')

# Create object by position

import OpenEXR
import amg_imath
import array
import maya.cmds as cmds
import time


def read_exr(filename, group_name, shape_name, scale):
    pt = amg_imath.PixelType(amg_imath.PixelType.FLOAT)
    exr_file = OpenEXR.InputFile(filename)

    # read RGB channel
    pos = []
    start_get_time = time.time()
    for c in 'RGB':
        position_str = exr_file.channel(c, pt)
        position = array.array('f', position_str).tolist()
        pos.append([val * scale for val in position if val != 0.0 in position])
    end_get_time = time.time()

    # create objects
    cmds.group(em=True, name=group_name)
    start_create_time = time.time()
    for i in range(len(pos[0])):
        p_name = shape_name + '_' + str(i)
        cmds.polyCube(n=p_name)
        cmds.setAttr(p_name + '.translate', pos[0][i], pos[1][i], pos[2][i])
        cmds.parent(p_name, group_name)        
    end_create_time = time.time()

    print"--- {} Get P time ---".format(end_get_time - start_get_time)
    print"--- {} Create objects time ---".format(end_create_time - start_create_time)


def start():
    exr_file = '//home/v.lavrentev/project/class/vfx_dev/openexr/position.exr'
    read_exr(exr_file, 'boxes', 'sphere', 10)

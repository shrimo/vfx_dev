"""
set Keyframe, create box by sinus

import sys
module_path = '/home/shrimo/Desktop/course/git/vfx_dev/maya/general_lesson'
if module_path not in sys.path:
    sys.path.append(module_path)
    

import lesson_v02
reload(lesson_v02)
lesson_v02.start()
"""


import maya.cmds as cmds
import math
import random


def set_key_frame(shape, a, b, c):
    for frame in xrange(1, 100):
        x_path = math.sin(float(frame * b)) * a
        z_path = float(frame * c)
        cmds.setKeyframe(shape, v=x_path, attribute='translateX',
                         time=frame)  # translateX
        cmds.setKeyframe(shape, v=z_path, attribute='translateZ',
                         time=frame)  # translateX
    return True


def create_sin_boxes(group_name, shape_name, a, b, c):
    cmds.group(em=True, name=group_name)
    for amount in xrange(1, 100):
        p_name = shape_name + '_' + str(amount)
        x_path = math.sin(float(amount * b)) * a
        z_path = float(amount * c)
        cmds.polyCube(n=p_name)  # create polyCube name by p_ + amount
        cmds.setAttr(p_name+'.translate', x_path, 0, z_path)
        cmds.group(p_name, parent=group_name)

    return True

def create_sphere_boxes(group_name, shape_name, r):
    cmds.group(em=True, name=group_name)
    for amount in xrange(1, 300):
        p_name = shape_name + '_' + str(amount)
        theta = random.uniform(0, 360)
        phi = 90 * (1 - math.sqrt(random.uniform(0, 1)))
        x_path = r * math.cos(theta)*math.sin(phi)
        y_path = r * math.sin(theta)*math.sin(phi)
        z_path = r * math.cos(phi)
        cmds.polyCube(n=p_name)  # create polyCube name by p_ + amount
        cmds.setAttr(p_name+'.translate', x_path, y_path, z_path)
        cmds.group(p_name, parent=group_name)

    return True


def start():
    # shapes = cmds.ls(selection=True, shapes=True, dagObjects=True)
    # m_name = 'motion_01'
    # cmds.polyCube(n=m_name)
    # print set_key_frame(m_name, 10, 0.3, 1)
    # create_sin_boxes('boxes', 'sin', 10, 0.3, 1)
    create_sphere_boxes('boxes', 'sphere', 10)

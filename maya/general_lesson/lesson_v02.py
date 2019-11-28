"""
set Keyframe

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


def set_key_frame(shape, a, b):
    for frame in xrange(1, 100):
        x_path = math.sin(float(frame * b)) * a
        z_path = float(frame)
        cmds.setKeyframe(shape, v=x_path, attribute='translateX',
                         time=frame)  # translateX
        cmds.setKeyframe(shape, v=z_path, attribute='translateZ',
                         time=frame)  # translateX
    return True


def start():
    # shapes = cmds.ls(selection=True, shapes=True, dagObjects=True)
    m_name = 'motion_04'
    cmds.polyCube(n=m_name)
    print set_key_frame(m_name, 5, 0.8)

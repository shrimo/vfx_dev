"""
get poly data(face center, face id, etc), select face, create object by face data

import sys
module_path = '/home/shrimo/Desktop/course/git/vfx_dev/maya/general_lesson'
if module_path not in sys.path:
    sys.path.append(module_path)
    

import lesson_v01
reload(lesson_v01)
lesson_v01.start()
"""


import maya.cmds as cmds
import maya.api.OpenMaya as om2


class Face():
    def __init__(self, shape, face_index, vertex, center):
        self.face_path = '{shape}.f[{index}]'.format(
            shape=shape,
            index=face_index)
        self.vertex = vertex
        self.face_index = face_index
        self.face_center = center


def l01():
    print(cmds.ls())
    print(cmds.ls(selection=True))
    return cmds.ls(selection=True, shapes=True, dagObjects=True)


def start():
    shapes = l01()
    # cmds.select(clear=True)
    print(shapes)
    shape_data = []
    for shape in shapes:
        mSel = om2.MSelectionList()
        mSel.add(shape)

        mDagPath, mObj = mSel.getComponent(0)
        geo = om2.MItMeshPolygon(mDagPath, mObj)
        while not geo.isDone():
            center = geo.center()
            # print center, geo.index()
            vertices = []
            for i in geo.getPoints(om2.MSpace.kWorld):
                vertices.append((i[0], i[1], i[2]))
            face_in = Face(shape, geo.index(), vertices, center)
            shape_data.append(face_in)
            geo.next(0)

    cmds.group(em=True, name='box01')
    for face in shape_data:
        print(face.face_index, face.face_path, face.face_center)
        if face.face_index & 1:
            cmds.select(face.face_path, add=True)
            p_name = 'p_'+str(face.face_index)
            cmds.polyCube(n=p_name)
            cmds.setAttr(p_name+'.scale', 0.2, 0.2, 0.2)
            cmds.setAttr(p_name+'.translate', face.face_center[0], face.face_center[1], face.face_center[2])
            cmds.select(all=True)
            cmds.group(p_name, parent='box01')
            cmds.select(all=True)

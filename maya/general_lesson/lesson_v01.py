"""
get poly data(face center, face id, etc), select face, create object by face data
setPosition for vertex (random)

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
import random


class Face():
    def __init__(self, shape, face_index, vertex, center):
        self.face_path = '{shape}.f[{index}]'.format(
            shape=shape,
            index=face_index)
        self.vertex = vertex
        self.face_index = face_index
        self.face_center = center


def get_shapes():
    # get selected object
    # print(cmds.ls())
    # print(cmds.ls(selection=True))
    return cmds.ls(selection=True, shapes=True, dagObjects=True)


def get_faces(shapes):
    # cmds.select(clear=True)
    # print(shapes)
    face_data = []
    for shape in shapes:
        mSel = om2.MSelectionList()
        mSel.add(shape)
        mDagPath, mObj = mSel.getComponent(0)
        geo = om2.MItMeshPolygon(mDagPath, mObj)
        while not geo.isDone():
            center = geo.center()
            print 'face index: {}'.format(geo.index())
            vertices = []
            for i in geo.getPoints(om2.MSpace.kWorld):
                vertices.append((i[0], i[1], i[2]))
            face_in = Face(shape, geo.index(), vertices, center)
            face_data.append(face_in)
            geo.next(0)

    return face_data

def get_vertex(shapes):
    vertex_data = []
    spc = om2.MSpace.kWorld
    for shape in shapes:
        mSel = om2.MSelectionList()
        mSel.add(shape)
        mDagPath, mObj = mSel.getComponent(0)
        vtx = om2.MItMeshVertex(mDagPath, mObj)
        while not vtx.isDone():
            vtx_pos = vtx.position(spc)
            print 'vertex index: {}'.format(vtx.index()), vtx_pos
            face_in = Face(shape, vtx.index(), vtx_pos, None)
            vertex_data.append(face_in)
            vtx.next()

    return vertex_data


def set_pos_vertex(shapes, up_y):
    spc = om2.MSpace.kWorld
    for shape in shapes:
        mSel = om2.MSelectionList()
        mSel.add(shape)
        mDagPath, mObj = mSel.getComponent(0)
        vtx = om2.MItMeshVertex(mDagPath, mObj)
        while not vtx.isDone():
            vtx_pos = vtx.position(spc)
            print 'vertex:'+str(vtx.index()), vtx_pos.y
            if vtx.index() & 1:
                vtx_pos.y += up_y
                vtx.setPosition(vtx_pos, spc)
            vtx.next()

        vtx.updateSurface()

def set_random_vertex(shapes, up_y):
    spc = om2.MSpace.kWorld
    for shape in shapes:
        mSel = om2.MSelectionList()
        mSel.add(shape)
        mDagPath, mObj = mSel.getComponent(0)
        vtx = om2.MItMeshVertex(mDagPath, mObj)
        while not vtx.isDone():
            vtx_pos = vtx.position(spc)
            print 'vertex:'+str(vtx.index()), vtx_pos.y
            vtx_pos.y += random.uniform(0, up_y)
            vtx.setPosition(vtx_pos, spc)
            vtx.next()

        vtx.updateSurface()

def create_boxes(shapes, group_name, shape_name, on_face):
    if on_face:
        face_data = get_faces(shapes)
    else:
        face_data = get_vertex(shapes)
    cmds.group(em=True, name=group_name)
    for face in face_data:
        # print(face.face_index, face.face_path, face.face_center)
        if face.face_index & 1:
            cmds.select(face.face_path, add=True)
            p_name = shape_name + str(face.face_index)
            cmds.polyCube(n=p_name) # create polyCube name by p_ + face index
            cmds.setAttr(p_name+'.scale', 0.5, 0.5, 0.5)
            if on_face:
                cmds.setAttr(p_name+'.translate', face.face_center[0], face.face_center[1], face.face_center[2])
            else:
                cmds.setAttr(p_name+'.translate', face.vertex.x, face.vertex.y, face.vertex.z)
            cmds.select(all=True)
            cmds.group(p_name, parent=group_name)
            cmds.select(all=True)

def start():
    # shapes = cmds.ls(selection=True, shapes=True, dagObjects=True)
    # set_pos_vertex(get_shapes(), 1)
    set_random_vertex(get_shapes(), 1)
    # create_boxes(get_shapes(), 'boxes', 'v_', 0)



"""
finding asymmetric polygons relative to X axis

import sys
module_path = '/home/shrimo/Desktop/course/git/vfx_dev/maya/general_lesson'
if module_path not in sys.path:
    sys.path.append(module_path)
    

import lesson_v03
reload(lesson_v03)
lesson_v03.maya_symmetry()
"""



from maya import cmds
from pprint import pprint
import maya.api.OpenMaya as om2
import time

TOLERANCE = 1e-4

def compare_vertices(vertices, opposite_vertices):
    '''
    Returns 0 if all vertices match
    '''
    
    for vertex in vertices:
        for opposite_vertex in opposite_vertices:
            if len(vertex) != len(opposite_vertex):
                return 0
            if (abs(vertex[0] + opposite_vertex[0]) < TOLERANCE
                    and abs(vertex[1] - opposite_vertex[1]) < TOLERANCE
                    and abs(vertex[2] - opposite_vertex[2]) < TOLERANCE):
                # Matched
                break
        else:
            # Not found
            break
    else:
        # Match
        return 0
    # No match
    return 1

def maya_symmetry():

    start_time = time.time()

    right_side = {}
    left_side = {}
    center_side = {}
    shapes = cmds.ls(selection=True, shapes=True, dagObjects=True)
    cmds.select(clear=True)    
        
    mSel = om2.MSelectionList()
 #   list_in = p_module.lo(shapes, om2)
  #  print list_in
    # return 0
    for shape in shapes:
        mSel.clear()
        mSel.add(shape)

        mDagPath, mObj = mSel.getComponent(0)
        # print type(mSel.getComponent(0)), mSel.getComponent(0)
        # print type(mDagPath), type(mObj), mDagPath, mObj
        # mFaceIter = om2.MItMeshFaceVertex(mDagPath, mObj)
        geo = om2.MItMeshPolygon(mDagPath, mObj)

        # while not geo.isDone():
        for j in range(geo.count()):
            # print geo.isDone(), geo.count()
            geo.setIndex(j)
            vertices = []
            center = geo.center(om2.MSpace.kWorld)
            # print type(center),center 
            slice_number = int(center[1]) # slice axis Y
            # print slice_number
            # print type(geo.getPoints(om2.MSpace.kWorld)), geo.getPoints(om2.MSpace.kWorld)
            for i in geo.getPoints(om2.MSpace.kWorld):
                vertices.append((i[0], i[1], i[2]))
            face_path = '{shape}.f[{index}]'.format(
                shape=shape,
                index=geo.index())
            if center[0] < -TOLERANCE:
                left_side.setdefault(slice_number, {})[face_path] = vertices
                print 'left side: ', vertices
            elif center[0] > TOLERANCE:
                right_side.setdefault(slice_number, {})[face_path] = vertices
                print 'right side: ', vertices
            else:
                center_side.setdefault(slice_number, {})[face_path] = vertices
                print 'centr side: ', vertices
            # geo.next(0)            
    # print geo.isDone()

    midle_time = time.time()
    
    non_symmetrical = []
    for slice_number, slice_faces in left_side.items():
        for face_id, vertices in slice_faces.items():
            opposite_slice_faces = right_side.get(slice_number, {})
            for opposite_face_id, opposite_vertices in opposite_slice_faces.items():
                if compare_vertices(vertices, opposite_vertices):
                    # No match
                    pass
                else:
                    # delete match opposite_slice_faces from dict
                    del opposite_slice_faces[opposite_face_id]
                    break
            else:
                # print '---------- Non-symmetric face:', face_id
                non_symmetrical.append(face_id)
                continue        

    start_check = time.time()

    for slice_number, slice_faces in right_side.items():
        for face_id, vertices in slice_faces.items():
            opposite_slice_faces = left_side.get(slice_number, {})
            for opposite_face_id, opposite_vertices in opposite_slice_faces.items():
                if compare_vertices(vertices, opposite_vertices):
                    # No match
                    pass
                else:
                    break
            else:
                # print '---------- Non-symmetric face:', face_id
                non_symmetrical.append(face_id)
                continue
    
    print 'Found', len(non_symmetrical), 'non symmetrical faces'
    cmds.select(non_symmetrical, add=True)

    print("--- %s seconds midle ---" % (midle_time - start_time))
    print("--- %s seconds midle 2 ---" % (start_check - midle_time))
    print("--- %s seconds first check ---" % (start_check - start_time))
    print("--- %s seconds next check ---" % (time.time() - start_check))
    print("--- %s seconds end ---" % (time.time() - start_time))    


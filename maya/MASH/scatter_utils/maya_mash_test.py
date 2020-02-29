'''
import sys
module_path = '/home/shrimo/Desktop/course/git/vfx_dev/maya/MASH'
if module_path not in sys.path:
    sys.path.append(module_path)
    

import maya_mash_test
reload(maya_mash_test)
maya_mash_test.main()
'''

__version__ = '1.0.5'

import os
import re
import sys
import copy
import math
import maya.cmds as cmds
import MASH.api as mapi
import maya.OpenMaya as om

# from amg.system import navigator
import imath
module_path = '/home/shrimo/Desktop/course/git/vfx_dev/maya/MASH/scatter_utils'
if module_path not in sys.path:
    sys.path.append(module_path)

import amg_scatter_utils
import time

import alembic.Abc as Abc
import alembic.AbcGeom as AbcGeom
import alembic.AbcCoreAbstract as AbcCoreAbstract


def _get_points_data(frame, node_name):
    '''
    Getting points data and matrix transformation
    '''
    # result = {}
    
    cmds.currentTime(frame, edit=True)
    sel = om.MSelectionList()
    sel.add(node_name)
    mash_node = om.MObject()
    sel.getDependNode(0, mash_node)
    mash_node_fn = om.MFnDependencyNode(mash_node)
    points_attribute = mash_node_fn.attribute('inputPoints')
    points_plug = om.MPlug(mash_node, points_attribute)
    handle_data = points_plug.asMDataHandle().data()
    input_points_data = om.MFnArrayAttrsData(handle_data)

    # get data from MASH (dict {index001:[m44f array]})
    matrix_mash = amg_scatter_utils.ocmash(input_points_data)

    return matrix_mash


def write_alembic(frames_data, node_name, obj_list, abc_path, list_frames):

    fps = 24.0
    oarchive = Abc.OArchive(abc_path, asOgawa=True)
    oroot = oarchive.getTop()
    xform = AbcGeom.OXform(oroot, str(node_name))
    ts = AbcCoreAbstract.TimeSampling(1 / fps, 1 / fps)
    tsidx = oroot.getArchive().addTimeSampling(ts)

    for obj_index, obj_name in enumerate(obj_list):
        print '', 'Object "{name}"'.format(name=obj_name)
        points = AbcGeom.OPoints(xform, obj_name, tsidx)
        arb = points.getSchema()
        arb_params = arb.getArbGeomParams()
        arb_matrix = Abc.OFloatArrayProperty(arb_params, 'Matrix4', tsidx)
        arb_index = Abc.OInt32ArrayProperty(arb_params, 'index', tsidx)
        for frame in list_frames:
            print 'Sample: {0} - write'.format(frame)
            points_data = frames_data[frame].get(obj_index)
            if points_data:
                points_number = len(points_data) / 16
                float_array = imath.FloatArray(points_number * 16)
                arr_index = imath.IntArray(points_number)
                ids = imath.IntArray(points_number)
                positions = imath.V3fArray(points_number)

                for i in range(0, points_number * 16, 16):
                    for j in range(16):
                        float_array[j + i] = points_data[j + i]

                    positions[i / 16] = imath.V3f(points_data[i + 12],
                                                  points_data[i + 13], points_data[i + 14])
                    arr_index[i / 16] = 0
                    ids[i / 16] = i / 16

                out_psamp = AbcGeom.OPointsSchemaSample()
                # add Ids data
                out_psamp.setIds(ids)
                # add Point positions data
                out_psamp.setPositions(positions)
                # add M44f data
                arb_matrix.setValue(float_array)
                # add Index pieces data
                arb_index.setValue(arr_index)
                points.getSchema().set(out_psamp)
            else:
                print 'Skipping "{node}", because there are no points'.format(node=obj_name)

    return True


def export(mash_nodes=None, scene_path=''):
    '''
    Export MASH node to alembic
    '''

    start_time_01 = time.time()

    if not mash_nodes:
        mash_nodes = cmds.ls(type=['MASH_Waiter'])
    if not isinstance(mash_nodes, list):
        mash_nodes = [mash_nodes]
    fps = 24.0
    # scene_path = scene_path or cmds.file(query=True, list=True)[0]
    # fields = navigator.fields_from_path(scene_path)
    # if not fields:
    #     print '[ERROR] Scene path not recognized: ' + scene_path
    #     return
    # root_path = ('//bstorage/strg01/mnt/projects/the_rising_hawk/'
    #              'assets/Environment/old_kiev/asm/publish/cache')
    frame_in = 1
    frame_out = 1
    list_frames = []
    current_frame = cmds.currentTime(update=False, query=True)
    cmds.refresh(suspend=True)
    for node_name in mash_nodes:
        print 'Processing MASH node: "{node}"'.format(node=node_name)
        mash_network = mapi.Network(node_name)
        node_ins = mash_network.instancer
        if cmds.objExists(node_name) and cmds.attributeQuery('anim', node=node_name, exists=True):
            anim_script = cmds.getAttr(node_name + '.anim')
            if anim_script is not None:
                # main:1-200
                frame_match = re.match(
                    r'(?P<name>\w+):(?P<in>\d+)-(?P<out>\d+)', anim_script)
                if frame_match:
                    frame_in = int(frame_match.group('in'))
                    frame_out = int(frame_match.group('out'))
                    list_frames = range(frame_in, frame_out + 1)
                    print '"{node}" has an animation sequence: "{script}"'.format(
                        node=node_name,
                        script=anim_script)
            else:
                print '"{node}" node does not have an animation'.format(node=node_name)
        if not list_frames:
            list_frames = [int(current_frame)]
        i = 0
        if node_ins.lower().endswith('_instancer'):
            input_name = '{node}.inputHierarchy'.format(node=node_ins)
            input_template = input_name + '[{index}]'
        else:
            input_name = '{node}.instancedGroup'.format(node=node_ins)
            input_template = input_name + '[{index}].instancedMesh[0].mesh'
        instance_indices = sorted(cmds.getAttr(
            input_name, multiIndices=True))
        obj_list = []
        for i in instance_indices:
            obj_list.append('asset_name_' + str(i))
        if not obj_list:
            print 'Skipping MASH node "{name}", no instanced objects found'.format(
                name=node_name)
            continue
        frames_data = {}
        for frame in list_frames:
            frames_data[frame] = _get_points_data(frame, node_name)
        # write alembic
        # node_name = re.sub(r'^MASH_?', '', node_name, flags=re.IGNORECASE)
        # abc_path = navigator.path_from_fields(
        #     fields,
        #     data_type='cache_scatter',
        #     update={
        #         'group': node_name.encode('ascii'),
        #     })
        abc_path = '/home/shrimo/Desktop/course/vfx_dev/alembic/mash_scatter.abc'
        # abc_path = os.path.dirname(__file__) + '/' + \
        #     node_name.encode('ascii') + '.abc'
        # if not os.path.isdir(os.path.dirname(abc_path)):
        #     os.makedirs(os.path.dirname(abc_path))

        if write_alembic(frames_data, node_name, obj_list, abc_path, list_frames):
            print 'Data saved to "{path}"'.format(path=abc_path)
        else:
            print 'Error'

    current_frame = cmds.currentTime(current_frame, update=False, edit=True)
    cmds.refresh(suspend=False)

    start_timePython_out = time.time() - start_time_01
    print 'time:', start_timePython_out
    print 'Export complete!'


def main():
    mash_nodes = cmds.ls(type=['MASH_Waiter'], selection=True) or cmds.ls(
        type=['MASH_Waiter'])
    if not mash_nodes:
        print 'No MASH nodes found'
        return
    export(mash_nodes)


if __name__ == '__main__':    
    main()

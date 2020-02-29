"""
Write alemic from MASH scatter


import sys
module_path = '/home/shrimo/Desktop/course/git/vfx_dev/maya/MASH'
if module_path not in sys.path:
    sys.path.append(module_path)


import write_abc
reload(write_abc)
write_abc.abc_main()

"""

import time
import maya.cmds as cmds
import MASH.api as mapi
import sys
import os

module_path = '/home/shrimo/project/amg_system/cpp'
if module_path not in sys.path:
    sys.path.append(module_path)

import lib_loader

def abc_main():
    mash_nodes_x = cmds.ls(type=['MASH_Waiter'], selection=True) or cmds.ls(type=['MASH_Waiter'])
    if not mash_nodes_x:
        print 'No MASH nodes found'
        return
    mash_nodes = str(mash_nodes_x[0])
    print 'MASH node: ', mash_nodes
    abc_path = '/home/shrimo/Desktop/course/vfx_dev/alembic/mash_scatter.abc'
    # if not os.path.isdir(abc_path):
    #     print ('no dir')
    #     return 0
    # abc_path = abc_path + 'mash_scatter.abc'
    obj_list = ['source', 'tree', 'bushes', 'grass']

    mashNetwork = mapi.Network(mash_nodes)
    node_ins = mashNetwork.instancer
    if node_ins.lower().endswith('_instancer'):
            input_name = '{node}.inputHierarchy'.format(node=node_ins)
            input_template = input_name + '[{index}]'
    else:
        input_name = '{node}.instancedGroup'.format(node=node_ins)
        input_template = input_name + '[{index}].instancedMesh[0].mesh'
    instance_indices = sorted(cmds.getAttr(input_name, multiIndices=True))
    instance_list = []
    for i in instance_indices:
        instance_list.append('tree_' + str(i))

    print instance_list
    # print 'animation: ', cmds.getAttr("defaultRenderGlobals.animation")

    start_C_time = time.time()
    lib_path = '/home/shrimo/Desktop/course/git/vfx_dev/maya/MASH/tmp/write_alembic.so'
    mash_cpp = lib_loader.call(mash_nodes, abc_path, instance_list,
                               lib=lib_path, func="mash2abc")
    # frame = 5
    # cmds.currentTime(25)
    # mash_cpp = cpp.call(frame, lib='write_alembic', func="maya_play")
    end_C_time = time.time()

    print mash_cpp[0]
    print mash_cpp[1]
    print("--- %s C++ time ---" % (end_C_time - start_C_time))


if __name__ == '__main__':
    abc_main()

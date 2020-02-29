__version__ = '1.0.1'

import os
import re
import copy
import sys
import math
import maya.cmds as cmds
import MASH.api as mapi
import maya.OpenMaya as om

from amg.system import navigator

amg_modules = '//bstorage/rep/set/scripts'
if amg_modules not in sys.path:
    sys.path.append(amg_modules)
from amg.system import cpp

def export(mash_nodes=None, scene_path=''):
    '''
    Export MASH node to alembic
    '''
    if not mash_nodes:
        mash_nodes = cmds.ls(type=['MASH_Waiter'])
    if not isinstance(mash_nodes, list):
        mash_nodes = [mash_nodes]
    fps = 24.0    
    
    for node_name in mash_nodes:
        print 'Processing MASH node: "{node}"'.format(node=node_name)
        mash_network = mapi.Network(node_name)
        node_ins = mash_network.instancer
        
        if cmds.objExists(node_name) and cmds.attributeQuery('anim', node=node_name, exists=True):
            anim_script = cmds.getAttr(node_name + '.anim')
            if anim_script is not None:
                # main:1-200
                frame_match = re.match(r'(?P<name>\w+):(?P<in>\d+)-(?P<out>\d+)', anim_script)
                if frame_match:
                    frame_in = int(frame_match.group('in'))
                    frame_out = int(frame_match.group('out'))
                    list_frames = range(frame_in, frame_out + 1)
                    print '"{node}" has an animation sequence: "{script}"'.format(
                        node=node_name,
                        script=anim_script)
            else:
                print '"{node}" node does not have an animation'.format(node=node_name)
      
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
            instance_obj = cmds.listConnections(input_template.format(index=i))                        
            obj_list.append(str(instance_obj[0]))            
      
        node_name_abc = re.sub(r'^MASH_?', '', node_name, flags=re.IGNORECASE)
        
        # mash_cpp = cpp.call(str(node_name), str(abc_path), obj_list, lib='write_alembic', func="mash2abc")
        mash_cpp = cpp.call(str(node_name), str('/home/v.lavrentev/project/speedtree/scene/mash/forest.abc'), obj_list, 
        lib='/home/v.lavrentev/project/rnd/write_alembic/write_alembic.so', func="mash2abc")

        print obj_list
        print node_name
        # print abc_path
      
    print 'Export complete!'

def main():
    mash_nodes = cmds.ls(type=['MASH_Waiter'], selection=True) or cmds.ls(type=['MASH_Waiter'])
    if not mash_nodes:
        print 'No MASH nodes found'
        return
    export(mash_nodes)

if __name__ == '__main__':
    main()

"""
finding asymmetric polygons relative to X axis

import sys
module_path = '/home/shrimo/project/rnd-master/symmetry'
if module_path not in sys.path:
    sys.path.append(module_path)
    

import symmetry
reload(symmetry)
symmetry.maya_symmetry()
"""

from maya import cmds
import time
import sys
module_path = '/home/shrimo/project/amg_system/cpp'
if module_path not in sys.path:
    sys.path.append(module_path)
import lib_loader

def _format_component(component_type, start=0, end=-1):
        '''
        Format a component
        '''
        if start != end or end > 0:
            return component_type + '[' + str(start) + ':' + str(end) + ']'
        return component_type + '[' + str(start) + ']'

def get_components_list(component_type, components):
    '''
    Get a list of components
    '''
    result = []
    start = -1
    previous = -1
    for component in sorted(components):
        if start < 0:
            start = component
            previous = component
            continue
        if component == previous + 1:
            previous = component
            continue
        if previous >= 0:
            result.append(_format_component(component_type, start, previous))
        previous = component
        start = component
    if previous >= 0:
        result.append(_format_component(component_type, start, previous))
    return result

def maya_symmetry():
    import os
    # print "ver 0.13"
    # path_lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'symmetry_check.so')
    # path_lib2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dll.so')

    shapes = cmds.ls(selection=True, shapes=True, dagObjects=True)
    print shapes
    bbox = cmds.exactWorldBoundingBox(shapes)
    print 'Bounding box ranges from: %f' % bbox[0], ', %f' % bbox[1], ', %f' % bbox[2],
    print ' to %f' % bbox[3], ', %f' % bbox[4], ', %f' % bbox[5]
    print 'height: ', bbox[4]

    cmds.select(clear=True)
    b_top = bbox[4];
   
    shapes_list = []
    for shape in shapes:        
        shapes_list.append(str(shape))        
  
    start_C_time = time.time()
    # print 1
    cpp_non_symmetrical = lib_loader.call(shapes_list, lib='/home/shrimo/project/rnd-master/symmetry/symmetry_check',
                                tolerance=0.0001, func="get_non_symmetrical")
    # print 2
    end_C_time = time.time()
    non_symmetrical = []
    print cpp_non_symmetrical['version']
    dict_map = cpp_non_symmetrical['non_symmetrical']

    for shape, components in dict_map.items():
        non_symmetrical += get_components_list(shape + '.f', components)

    print 'Found c++', len(non_symmetrical), 'non symmetrical faces'
    cmds.select(non_symmetrical, add=True)
    end2_C_time = time.time()

    print("--- %s C++ time ---" % (end_C_time  - start_C_time))
    print("--- %s select time ---" % (end2_C_time  - end_C_time))
    
    # print non_symmetrical

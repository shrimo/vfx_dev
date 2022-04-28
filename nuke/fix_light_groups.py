# The features of the current pipeline, 
# the accumulated light groups do not equal the beauty pass. 
# This script automates the process of getting the difference 
# and recording it into a separate light group.


# import sys
# module_path = '/home/vfx/.nuke'
# if module_path not in sys.path:
#     sys.path.append(module_path)

# import auto_compositing
# reload(auto_compositing)
# auto_compositing.start()

# add for install
# nuke.menu('Nuke').addCommand('PipelineTools/fix_light_groups', lambda: fix_light_groups.start())
# nuke.menu('Nuke').addCommand('PipelineTools/auto_compositing', lambda: auto_compositing.start())

import nuke

def get_light_group(node):    
    channels = node[0].channels()
    all_layers = list(set([c.split('.')[0] for c in channels]))
    light_group = []
    for layer in all_layers:
      if 'light' in layer:
          light_group.append(layer)
    return sorted(light_group)


def light_group_fix(node, light_group):
    dot = nuke.createNode('Dot')
    dot.setInput(0, node[0])

    nuke.Layer('cd_tmp', ['cd_tmp.red', 'cd_tmp.green', 'cd_tmp.blue'])
    nuke.Layer('light_fix', ['light_fix.red', 'light_fix.green', 'light_fix.blue'])

    merge_group_start = nuke.createNode('Merge2')
    merge_group_start.setInput(1, dot)
    merge_group_start.setInput(0, dot)
    merge_group_start['operation'].setValue('plus')
    merge_group_start['Achannels'].setValue(light_group.pop())
    merge_group_start['Bchannels'].setValue(light_group.pop())
    merge_group_start['output'].setValue('cd_tmp')

    dot = nuke.createNode('Dot')
    dot.setInput(0, merge_group_start)

    for i in range(len(light_group)):
        merge_group_next = nuke.createNode('Merge2')
        merge_group_next.setInput(1, dot)
        merge_group_next.setInput(0, dot)
        merge_group_next['operation'].setValue('plus')
        merge_group_next['Achannels'].setValue('cd_tmp')
        merge_group_next['Bchannels'].setValue(light_group[i])
        merge_group_next['output'].setValue('cd_tmp')

        dot = nuke.createNode('Dot')
        dot.setInput(0, merge_group_next)

    merge_minus = nuke.createNode('Merge2')
    merge_minus.setInput(1, dot)
    merge_minus.setInput(0, dot)
    merge_minus['operation'].setValue('minus')
    merge_minus['Achannels'].setValue('rgb')
    merge_minus['Bchannels'].setValue('cd_tmp')
    merge_minus['output'].setValue('light_fix')
    return True



def start():
    node = nuke.selectedNodes()
    if node:
        light_group = get_light_group(node)    
        lg_comp = light_group_fix(node, light_group)
    else:
        nuke.message('Select node')
        

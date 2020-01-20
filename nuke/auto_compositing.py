# Light group compositing

def get_light_group(node):    
    channels = node[0].channels()
    all_layers = list(set([c.split('.')[0] for c in channels]))
    light_group = []
    for layer in all_layers:
      if 'light' in layer:
          light_group.append(layer)
    return sorted(light_group)


def light_group_comp(node, light_group):
    dot = nuke.createNode('Dot')
    dot.setInput(0, node[0])    
    merge_group_start = nuke.createNode('Merge2')
    merge_group_start.setInput(1, dot)
    merge_group_start.setInput(0, dot)
    merge_group_start['operation'].setValue('plus')
    merge_group_start['Achannels'].setValue(light_group.pop())
    merge_group_start['Bchannels'].setValue(light_group.pop())
    dot = nuke.createNode('Dot')
    dot.setInput(0, merge_group_start)
    for i in range(len(light_group)):        
        merge_group_next = nuke.createNode('Merge2')
        merge_group_next.setInput(1, dot)
        merge_group_next.setInput(0, dot)
        merge_group_next['operation'].setValue('plus')
        merge_group_next['Achannels'].setValue('rgb')
        merge_group_next['Bchannels'].setValue(light_group[i])
        dot = nuke.createNode('Dot')
        dot.setInput(0, merge_group_next)
        merge_group_start = dot
    return True


node = nuke.selectedNodes()
if node:
    light_group = get_light_group(node)    
    lg_comp = light_group_comp(node, light_group)
else:
    nuke.message('Select node')
# read from 3dequalizer track

def create_track():
    t_node = nuke.createNode('Transform')
    k = t_node['translate']
    k.setAnimated()
    return k, t_node

flag = 1
filepath = '/home/v.lavrentev/project/class/eq_to_nuke/for_python.txt'
with open(filepath) as fp:    
    for line in fp:        
        if len(line.split(' ')) == 3:
            track = line.split(' ')
            nuke.activeViewer().frameControl(int(track[0]))
            X = float(track[1]) - t_node['center'].getValue()[0]
            Y = float(track[2]) - t_node['center'].getValue()[1]
            k.setValueAt(X, int(track[0]), 0)
            k.setValueAt(Y, int(track[0]), 1)
            flag = 1
        else:
            if flag:
                flag = 0
                k, t_node = create_track()

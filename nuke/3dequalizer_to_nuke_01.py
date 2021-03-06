# read from 3dequalizer track
import threading


def create_track():
    """
    Return a transform node
    """
    t_node = nuke.createNode('Transform')
    k = t_node['translate']
    k.setAnimated()
    return k, t_node

def get_track_data(filepath):
    task = nuke.ProgressTask('Read track data...')
    filepath = '/home/v.lavrentev/project/class/eq_to_nuke/for_python.txt'
    with open(filepath, "r") as fp:
        tracks_count = int(fp.readline().split('\n')[0]) # read first line in file. tracks count
        print 'tracks count:', tracks_count
        for block in range(tracks_count):
            track_namber = int(fp.readline().split('\n')[0]) # tracks number
            offset = int(fp.readline().split('\n')[0]) # frame offset
            frame_range = int(fp.readline().split('\n')[0]) # frame range (time)
            k, t_node = create_track() # create transform node for track
            prog_incr = 100.0 / tracks_count
            if task.isCancelled():
                nuke.executeInMainThread(nuke.message, args=('Aborted',))
                return
            task.setProgress(int(block * prog_incr)) # indicator for progress bar
            for frame in range(frame_range):
                track = fp.readline().split(' ') # read track data number track, X, Y
                X = float(track[1]) - t_node['center'].getValue()[0] # move X by cetner
                Y = float(track[2]) - t_node['center'].getValue()[1] # move Y by cetner
                k.setValueAt(X, int(track[0]), 0) # set keyframe for X
                k.setValueAt(Y, int(track[0]), 1) # set keyframe for Y
    

filepath = '/home/v.lavrentev/project/class/eq_to_nuke/for_python_min.txt'
threading.Thread(target=get_track_data, args=(filepath, )).start()

# List alebic object
import os
import sys
import alembic
import time


def find_node(obj, name):
    for index in xrange(obj.getNumChildren()):
        child = obj.getChild(index)
        if child.getName() == name:
            return child
        child = find_node(child, name)
        if child:
            return child
    return None


def list_object(i_obj):
    for index in xrange(i_obj.getNumChildren()):
        i_child = i_obj.getChild(index)
        if str(i_child).count('/') > 1:
            print ' ' * str(i_child).count('/'), i_child    
        else:
            print i_child
        i_child_name = i_child.getName()
        list_object(i_child)


def list_abc(i_path):
    '''
    List alembic object
    '''
    if not os.path.isfile(i_path):
        print 'No file:', i_path
        return None

    i_archive = alembic.Abc.IArchive(i_path)
    start = time.time()
    info = alembic.Abc.GetArchiveInfo(i_archive)
    # print info
    if len(info['appName']) > 0:
        print 'app name: {}'.format(info['appName'])
        print 'library version: {}'.format(info['libraryVersionString'])
        print 'when written: {}'.format(info['whenWritten'])
        print 'user description: {}'.format(info['userDescription'])
    else:
        print i_archive.getTop(), '- file doesnt have any ArchiveInfo'

    print i_archive.getTop().getName()

    list_object(i_archive.getTop())

    end = time.time()
    print '\ntime: ', end - start

if __name__ == '__main__':
    list_abc(sys.argv[1])

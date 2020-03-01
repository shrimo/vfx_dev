# Alembic Separation (extracting a separate node from the archive)
import os
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


def copy_props(i_props, o_props, animation):
    for index in xrange(i_props.getNumProperties()):
        header = i_props.getPropertyHeader(index)
        # print 'header: ', header.getName()

        if header.isArray():
            i_prop = alembic.Abc.IArrayProperty(i_props, header.getName())
            o_prop = alembic.Abc.OArrayProperty(
                o_props, i_prop.getName(), i_prop.getDataType(), i_prop.getMetaData(), 0)
            o_prop.setTimeSampling(i_prop.getTimeSampling())

            for index in xrange(i_prop.getNumSamples()):
                # sel = alembic.Abc.ISampleSelector(index)
                o_prop.setValue(i_prop.getValue(index))
                if not animation:
                    break

        elif header.isScalar():
            i_prop = alembic.Abc.IScalarProperty(i_props, header.getName())
            o_prop = alembic.Abc.OScalarProperty(
                o_props, i_prop.getName(), i_prop.getDataType(), i_prop.getMetaData(), 0)
            o_prop.setTimeSampling(i_prop.getTimeSampling())

            for index in xrange(i_prop.getNumSamples()):
                # sel = alembic.Abc.ISampleSelector(index)
                o_prop.setValue(i_prop.getValue(index))
                if not animation:
                    break

        elif header.isCompound():
            i_prop = alembic.Abc.ICompoundProperty(i_props, header.getName())
            o_prop = alembic.Abc.OCompoundProperty(
                o_props, i_prop.getName(), i_prop.getMetaData())
            copy_props(i_prop, o_prop, animation)


def check_faceset(obj):
    p_obj = obj.getProperties()
    for index in xrange(p_obj.getNumProperties()):
        header = p_obj.getPropertyHeader(index)
        if header.getName() == '.faceset':
            return True
    return False


def copy_object(i_obj, o_obj, animation, root, skip_node):

    i_props = i_obj.getProperties()
    o_props = o_obj.getProperties()
    copy_props(i_props, o_props, animation)

    for index in xrange(i_obj.getNumChildren()):
        i_child = i_obj.getChild(index)
        if check_faceset(i_child):
            continue
        i_child_name = i_child.getName()
        if i_child_name in skip_node:
            continue
        # if i_child_name == root:
        #     i_child_name = 'mdl'
        oChild = alembic.Abc.OObject(
            o_obj,
            i_child_name.lower(),
            i_child.getMetaData())
        copy_object(i_child, oChild, animation, root, skip_node)


def main():
    i_path = '/home/shrimo/Desktop/course/vfx_dev/alembic/abc_separation_03_in.abc'
    o_path = '/home/shrimo/Desktop/course/vfx_dev/alembic/abc_separation_03_out.abc'

    if not os.path.isfile(i_path):
        print 'No file:', i_path
        return None

    i_archive = alembic.Abc.IArchive(i_path)
    o_archive = alembic.Abc.OArchive(o_path, asOgawa=True)

    for index in xrange(i_archive.getNumTimeSamplings()):
        o_archive.addTimeSampling(i_archive.getTimeSampling(index))

    animation = True
    i_top = i_archive.getTop()
    root = i_top.getChild(0).getName()

    skip_list = ['pcone1', 'ptorus1']
    # skip_list = ['pTorus1']

    skip_node_list = []
    for skip in skip_list:
        skip_node_list.append(find_node(i_top, skip).getName())
    print 'Find node: ', skip_node_list
    start = time.time()

    copy_object(i_archive.getTop(), o_archive.getTop(),
                animation, root, skip_node_list)

    end = time.time()
    print 'Separation successful'
    print 'time: ', end - start

# main()
if __name__ == '__main__':
    main()

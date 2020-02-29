#!/usr/bin/env python2.7
import imath
import alembic.Abc as Abc
import alembic.AbcGeom as AbcGeom
import alembic.AbcCoreAbstract as AbcCoreAbstract
import alembic.Util as Util


def get_matrix(i_list):
    i_matrix = imath.M44d()
    l = 0
    for y in range(0, 4):
        for x in range(0, 4):
            i_matrix[y][x] = i_list[l]
            l += 1
    i_matrix.invert()
    return i_matrix


def copy_xform(iProps, oProps, i_list):
    for index in xrange(iProps.getNumProperties()):
        header = iProps.getPropertyHeader(index)
        # print "header: ", header.getName()

        if header.isCompound():
            iProp = Abc.ICompoundProperty(iProps, header.getName())
            oProp = Abc.OCompoundProperty(
                oProps, iProp.getName(), iProp.getMetaData())
            # print 'isCompound: ', header.getName()
            if header.getName() == ".xform":
                # print "getNumProperties: ", iProp.getNumProperties()
                if iProp.getNumProperties() == 0:
                    # print "no .vals"
                    m_oProp = Abc.OScalarProperty(
                        oProp, '.vals', Abc.M44dTPTraits.dataType(), 0, 1)
                    # i_list = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 200, 200, 200, 1]
                    i_matrix = get_matrix(i_list)
                    m_oProp.setValue(i_matrix)

                    i_oProp = Abc.OScalarProperty(
                        oProp, '.inherits', Abc.BooleanTPTraits.dataType(), 0, 1)
                    i_oProp.setValue(True)

                    ops_oProp = Abc.OScalarProperty(
                        oProp, '.ops', Abc.Uint8TPTraits.dataType(), 0, 1)
                    ops_oProp.setValue(48)

                else:
                    for idx in xrange(iProp.getNumProperties()):
                        header = iProp.getPropertyHeader(idx)
                        # print ".xform header: ", header.getName()
                        if header.getName() == ".vals":
                            # print "--- matrix --- 01"
                            x_iProp = Abc.IScalarProperty(
                                iProp, header.getName())
                            x_oProp = Abc.OScalarProperty(oProp, x_iProp.getName(), Abc.M44dTPTraits.dataType(),
                                                          x_iProp.getMetaData(), x_iProp.getTimeSampling())
                            # i_list = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 2, 2, 2, 1]
                            i_matrix = get_matrix(i_list)
                            # print i_matrix
                            x_oProp.setValue(i_matrix)

                        elif header.getName() == ".ops":
                            ops_oProp = Abc.OScalarProperty(
                                oProp, '.ops', Abc.Uint8TPTraits.dataType(), 0, 1)
                            ops_oProp.setValue(48)

                        else:
                            if header.isScalar():
                                y_iProp = Abc.IScalarProperty(
                                    iProp, header.getName())
                                y_oProp = Abc.OScalarProperty(oProp, y_iProp.getName(), y_iProp.getDataType(),
                                                              y_iProp.getMetaData(), y_iProp.getTimeSampling())
                                sel = Abc.ISampleSelector(
                                    y_iProp.getNumSamples())
                                y_oProp.setValue(y_iProp.getValue(sel))


def copyProps(iProps, oProps):
    for index in xrange(iProps.getNumProperties()):
        header = iProps.getPropertyHeader(index)

        if header.isArray():
            iProp = Abc.IArrayProperty(iProps, header.getName())
            oProp = Abc.OArrayProperty(oProps, iProp.getName(), iProp.getDataType(
            ), iProp.getMetaData(), iProp.getTimeSampling())

            sel = Abc.ISampleSelector(iProp.getNumSamples())
            # print index, sel
            oProp.setValue(iProp.getValue(sel))

        elif header.isScalar():
            iProp = Abc.IScalarProperty(iProps, header.getName())
            oProp = Abc.OScalarProperty(oProps, iProp.getName(), iProp.getDataType(
            ), iProp.getMetaData(), iProp.getTimeSampling())

            sel = Abc.ISampleSelector(iProp.getNumSamples())
            oProp.setValue(iProp.getValue(sel))

        elif header.isCompound():
            iProp = Abc.ICompoundProperty(iProps, header.getName())
            oProp = Abc.OCompoundProperty(
                oProps, iProp.getName(), iProp.getMetaData())
            copyProps(iProp, oProp)


def copyObject(iObj, oObj, ix, i_list):
    iProps = iObj.getProperties()
    oProps = oObj.getProperties()

    if ix == 1:
        copy_xform(iProps, oProps, i_list)
        # print 'matrix 01'
    else:
        copyProps(iProps, oProps)
    # print ix

    for index in xrange(iObj.getNumChildren()):
        iChild = iObj.getChild(index)
        oChild = Abc.OObject(oObj, iChild.getName(), iChild.getMetaData())
        ix += 1
        # print oChild.getName()
        copyObject(iChild, oChild, ix, i_list)


def main():
    # iPath = "/fstorage/projects/mavka/sequences/ep0250/ep0250_sh0010/abc/anm/frol-mdl.abc"
    # iPath = "/fstorage/projects/mavka/sequences/ep0250/ep0250_sh0010/abc/cfx/frol-mdl.abc"
    # iPath = "/home/v.lavrentev/projects/alembic/abctools/samples.abc"
    iPath = "/fstorage/projects/mavka/sequences/ep0255/ep0255_sh0050/abc/anm/dressing_table_ar-mdl.abc"
    oPath = "/home/v.lavrentev/project/samples_out.abc"
    iArchive = Abc.IArchive(iPath)
    oArchive = Abc.OArchive(oPath)

    for index in xrange(iArchive.getNumTimeSamplings()):
        oArchive.addTimeSampling(iArchive.getTimeSampling(index))

    IAbc = iArchive.getTop()
    OAbc = oArchive.getTop()

    i_list = [-0.9995150870889227, 0.0, 0.031138251100918873, 0.0, 0.0, 1.0, 0.0, 0.0, -0.031138251100918873,
              0.0, -0.9995150870889227, 0.0, -2.270938345653162, -0.12584946304559708, 482.26168727874756, 1.0]

    copyObject(IAbc, OAbc, 0, i_list)


if __name__ == '__main__':
    main()

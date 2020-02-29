import alembic

def copyProps(iProps, oProps):
    for index in xrange(iProps.getNumProperties()):
        header = iProps.getPropertyHeader(index)

        if header.isArray():
            iProp = alembic.Abc.IArrayProperty(iProps, header.getName())
            oProp = alembic.Abc.OArrayProperty(oProps, iProp.getName(), iProp.getDataType(), iProp.getMetaData(), 0)

            # for index in xrange(iProp.getNumSamples()):
            sel = alembic.Abc.ISampleSelector(0)
            oProp.setValue(iProp.getValue(sel))

        elif header.isScalar():
            iProp = alembic.Abc.IScalarProperty(iProps, header.getName())
            oProp = alembic.Abc.OScalarProperty(oProps, iProp.getName(), iProp.getDataType(), iProp.getMetaData(), 0)

            # for index in xrange(iProp.getNumSamples()):
            sel = alembic.Abc.ISampleSelector(0)
            oProp.setValue(iProp.getValue(sel))

        elif header.isCompound():
            iProp = alembic.Abc.ICompoundProperty(iProps, header.getName())
            oProp = alembic.Abc.OCompoundProperty(oProps, iProp.getName(), iProp.getMetaData())
            copyProps(iProp, oProp)


def copyObject(iObj, oObj):
    iProps = iObj.getProperties()
    oProps = oObj.getProperties()
    copyProps(iProps, oProps)

    for index in xrange(iObj.getNumChildren()):
        iChild = iObj.getChild(index)
        oChild = alembic.Abc.OObject(oObj, iChild.getName(), iChild.getMetaData())
        copyObject(iChild, oChild)


def main():
    iPath = "/home/v.lavrentev/project/alembic/a_test.abc"
    oPath = "/home/v.lavrentev/project/alembic/a_test_out4.abc"
    iArchive = alembic.Abc.IArchive(iPath)
    oArchive = alembic.Abc.OArchive(oPath, asOgawa=True)

    # for index in xrange(iArchive.getNumTimeSamplings()):
    #     oArchive.addTimeSampling(iArchive.getTimeSampling(index))

    copyObject(iArchive.getTop(), oArchive.getTop())

    print 'ok - ', oPath


if __name__ == '__main__':
    main()

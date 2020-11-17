import imath
import alembic.Abc as Abc
import alembic.AbcGeom as AbcGeom
import alembic.AbcCoreAbstract as AbcCoreAbstract
import random as rnd

def FloatArrayM44d(floatarray, pointnums):
    ''' 
    convert data floatarray -> m44d
    '''
    inMatrix44Array = []
    l = 0
    for n in range(pointnums):        
        inMatrix44Array.append(imath.M44d())        
        for y in range(0, 4):
            for x in range(0, 4):
                inMatrix44Array[n][y][x] = floatarray[l]
                l += 1
    return inMatrix44Array


def getFloatArray (finename):
    ''' 
    load data floatarray (16)
    out floatarray and floatarray size / 16 (M44f)
    '''

    archiveI = Abc.IArchive(finename) # read alembic file *.abc
    print 'Archive valid ->', archiveI.valid()

    RtopObj = archiveI.getTop() # root lavel
    print 'Top name ->', RtopObj.getName(), RtopObj.getNumChildren()

    childObj = RtopObj.children[0] # get children object
    childrenSplit = str(childObj.children[0]).split('/') # fing AbcGeom Points
    print 'Children ->', childrenSplit[-1], childObj.getNumChildren()

    points = AbcGeom.IPoints(childObj, childrenSplit[-1]) # IPoints geometric interpretation
    print 'Schema title ->', points.getSchemaTitle()

    ipo = points.getProperties()
    print ipo.propertyheaders[0]
    ingeo = ipo.getProperty(str(ipo.propertyheaders[0]))
    for pname in ingeo.propertyheaders: # find .arbGeomParams
        #print pname, pname.getDataType()
        if str(pname.getDataType()) == 'UNKNOWN':
            arb = ingeo.getProperty(str(pname))

    inM44f = arb.getProperty('Matrix4')
    print inM44f.getName(), 'number of m44f ->', len(inM44f.samples[0]) / 16

    for x in inM44f.samples:
        ArrM44f = imath.FloatArray(len(x))
        for i, y in enumerate(x):
            #print  y,
            ArrM44f[i] = y  #.append(y)
    return ArrM44f, len(inM44f.samples[0]) / 16


def copyProps(iProps, oProps):
    for index in xrange(iProps.getNumProperties()):
        header = iProps.getPropertyHeader(index)

        if header.isArray():
            iProp = Abc.IArrayProperty(iProps, header.getName())
            oProp = Abc.OArrayProperty(oProps, iProp.getName(), iProp.getDataType(), iProp.getMetaData(), iProp.getTimeSampling())

            for index in xrange(iProp.getNumSamples()):
                sel = Abc.ISampleSelector(index)
                oProp.setValue(iProp.getValue(sel))

        elif header.isScalar():
            iProp = Abc.IScalarProperty(iProps, header.getName())
            oProp = Abc.OScalarProperty(oProps, iProp.getName(), iProp.getDataType(), iProp.getMetaData(), iProp.getTimeSampling())

            for index in xrange(iProp.getNumSamples()):
                sel = Abc.ISampleSelector(index)
                oProp.setValue(iProp.getValue(sel))

        elif header.isCompound():
            iProp = Abc.ICompoundProperty(iProps, header.getName())
            oProp = Abc.OCompoundProperty(
                oProps, iProp.getName(), iProp.getMetaData())
            copyProps(iProp, oProp)


def abcInstance(topObj, source, outM44d, arraySize):
    instnum = int(arraySize)
    #print instnum
    XFormInst = []
    for i in range(1, instnum):
        XFormInst.append(AbcGeom.OXform(topObj, 'geoInst_{0}'.format(i)))
        XFormInst[i-1].addChildInstance(source, 'OUT')        

    XSampOut = []
    for i in range(1, instnum):
        XSampOut.append(AbcGeom.XformSample())
        XSampOut[i-1].setMatrix(outM44d[i])   
        XFormInst[i-1].getSchema().set(XSampOut[i-1])
        #print i,
    print '- Instance is ready -'

def copyObject(iObj, oObj, rootName, pPath):
    iProps = iObj.getProperties()
    oProps = oObj.getProperties()
    copyProps(iProps, oProps)

    for index in xrange(iObj.getNumChildren()):
        iChild = iObj.getChild(index)

        if iChild.getName() == rootName:
            PointCloudFile = pPath # "/home/v.lavrentev/projects/alembic/alembicInstance_out.abc" # Point Cloud File
            inFloatArray, arraySize = getFloatArray(PointCloudFile)
            outM44d = FloatArrayM44d(inFloatArray, arraySize)

            XFormRoot = AbcGeom.OXform(oObj, 'RootInst')
            # set Xform matrix for first element
            XFRsamp = AbcGeom.XformSample()            
            XFRsamp.setMatrix(outM44d[0])
            XFormRoot.getSchema().set(XFRsamp)

            oChild = Abc.OObject(XFormRoot, iChild.getName(), iChild.getMetaData())
            abcInstance(oObj, oChild, outM44d, arraySize)  # add instanc XForm
            copyObject(iChild, oChild, rootName, pPath)

            print oChild.getName(), ' - root - ', iChild.getMetaData()

        else:
            oIChild = Abc.OObject(oObj, iChild.getName(), iChild.getMetaData())
            copyObject(iChild, oIChild, rootName, pPath)
            # print oIChild.getName(),' - - - ', iChild.getMetaData()


def main():
    # List from asset and pointClouds
    mainPath = '/home/alembic/AbcMaterial/tree/'
    treeList = ['treeOak.abc', 'treePine.abc', 'treePoplar.abc']
    iPathArray = []
    oPathArray = []
    pPathArray = []
    
    for i, iname in enumerate(treeList):
        iPathArray.append (mainPath + iname)
        oPathArray.append (mainPath + 'geoInst_' + iname)
        pPathArray.append (mainPath + 'pcloud_' + iname)
        #print iPathArray[i]
        #print oPathArray[i]
        #print pPathArray[i]
    
    for i in range(len(treeList)):        
        iArchive = Abc.IArchive(iPathArray[i])
        oArchive = Abc.OArchive(oPathArray[i], asOgawa=True)
    
        for index in xrange(iArchive.getNumTimeSamplings()):
            oArchive.addTimeSampling(iArchive.getTimeSampling(index))

        IAbc = iArchive.getTop()
        OAbc = oArchive.getTop()
        childName = IAbc.children[0] # get first child name (mdl, prx)
        childrenSplit = str(childName).split('/')
        print 'First child: ', childrenSplit[-1]

        copyObject(IAbc, OAbc, childrenSplit[-1], pPathArray[i])


if __name__ == '__main__':    
    main()

import imath
import alembic.Abc as Abc
import alembic.AbcGeom as AbcGeom


class AbcReplicate(Abc.IArchive):
    '''
    Merge multiple alembic files (infile_01.abc, infile_01.abc to outfile_02.abc)
    '''

    def __init__(self, abcIPath='abc.abc', abcOPath='abc.abc'):
        super(AbcReplicate, self).__init__(abcIPath)
        self.instCounter = 0
        self.abcIPath = abcIPath
        self.abcOPath = abcOPath       
        self.iArchive = Abc.IArchive(self.abcIPath)
        self.oArchive = Abc.OArchive(self.abcOPath, asOgawa=True)
        self.iAbc = self.iArchive.getTop()
        self.oAbc = self.oArchive.getTop()        
        print self.iAbc.getChild(0).getName()  # root obj

    def nextFile(self, abcIPath):
        self.abcIPath = abcIPath
        self.iArchive = Abc.IArchive(self.abcIPath)
        self.iAbc = self.iArchive.getTop()        
        print self.iAbc.getChild(0).getName()

    def Replicate(self):
        self.oInst = AbcGeom.OXform( self.oAbc, 'parent_' + str(self.instCounter) )
        self.copyObj(self.iAbc, self.oInst)
        self.instCounter += 1

    def copyProps(self, iProps, oProps):
        for index in xrange(iProps.getNumProperties()):
            header = iProps.getPropertyHeader(index)

            if header.isArray():
                iProp = Abc.IArrayProperty(iProps, header.getName())
                oProp = Abc.OArrayProperty(oProps, iProp.getName(), iProp.getDataType(),
                                           iProp.getMetaData(), iProp.getTimeSampling())

                for index in xrange(iProp.getNumSamples()):
                    sel = Abc.ISampleSelector(index)
                    oProp.setValue(iProp.getValue(sel))

            elif header.isScalar():
                iProp = Abc.IScalarProperty(iProps, header.getName())
                oProp = Abc.OScalarProperty(oProps, iProp.getName(), iProp.getDataType(),
                                            iProp.getMetaData(), iProp.getTimeSampling())

                for index in xrange(iProp.getNumSamples()):
                    sel = Abc.ISampleSelector(index)
                    oProp.setValue(iProp.getValue(sel))

            elif header.isCompound():
                iProp = Abc.ICompoundProperty(iProps, header.getName())
                oProp = Abc.OCompoundProperty(
                    oProps, iProp.getName(), iProp.getMetaData())
                self.copyProps(iProp, oProp)

    def copyObj(self, iObj, oObj):
        iProps = iObj.getProperties()
        oProps = oObj.getProperties()
        self.copyProps(iProps, oProps)
        for index in xrange(iObj.getNumChildren()):
            iChild = iObj.getChild(index)
            oChild = Abc.OObject(oObj, iChild.getName(), iChild.getMetaData())
            #print index, iChild.getName()
            self.copyObj(iChild, oChild)


pPath = '/home/alembic/abc/'
iFile = []
iFile.append( pPath + 'hierarchy.abc' )
iFile.append( 'tree01.abc' )
iFile.append( 'tree02.abc' )
iFile.append( 'tree03.abc' )
iFile.append( 'tree04.abc' )
oFile = pPath + 'hierarchy_merge.abc'

print iFile[0]
aRep = AbcReplicate(iFile[0], oFile)
aRep.Replicate()
for i in range(1, len(iFile)):
    aRep.nextFile(iFile[i])
    aRep.Replicate()

import imath
import alembic.Abc as Abc
import alembic.AbcGeom as AbcGeom


def get_attribut(abc_path, node):

    iArchive = Abc.IArchive(abc_path)
    iAbc = iArchive.getTop()
    # ixf = AbcGeom.IXform(iAbc, str(iAbc.children[0]).split('/')[-1])
    ixf = AbcGeom.IXform(iAbc, 'flowers')
    ipoints = AbcGeom.IPoints(ixf, node)
    arbattrs = ipoints.getSchema().getArbGeomParams()

    max_index = 0
    for samp in arbattrs.getProperty('index').samples:
        max_index = max(max_index, max(samp))

    print max_index
        

node = 'trunk'
abc_path = 'tree.abc'
get_attribut(abc_path, node)



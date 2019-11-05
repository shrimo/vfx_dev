import os

# load alembic
iFileName = '01.abc'
alembic_list = ['Abc', 'AbcCollection', 'AbcCoreAbstract', 'AbcGeom', 'AbcMaterial',
                'Util', '__doc__', '__file__', '__name__', '__package__', '__path__']
try:
    import alembic
    assert dir(alembic) == alembic_list
    assert os.path.isfile(iFileName)
    alembic_test = alembic.Abc.IArchive(iFileName)
    assert alembic_test.getTop().children[0].getName() == 'group1'
except Exception as e:
    print 'non load alembic'

# load imath
try:
    import imath
    matrix = imath.M44f()
    for y in range(0, 4):
        for x in range(0, 4):
            matrix[y][x] = 3.14

    assert matrix[0][0], 3.14
    assert matrix.translation() == imath.V3f(3.14, 3.14, 3.14)
except Exception as e:
    print 'non load imath'

#  load numpy
try:
    import numpy
    A = numpy.array([1., 2.])
    assert numpy.allclose(A, [1., 2.])

except Exception as e:
    print 'non load numpy'


#  load OpenCV
try:
    import cv2
    assert os.path.isfile('bg.jpg')
    img = cv2.imread('bg.jpg')
    img_blur = cv2.blur(img, (15, 15))
    assert img[0][0][0] == 96
    assert img_blur[0][0][0] == 75
    cv2.imwrite('blur_bg.jpg', img_blur)
    assert os.path.isfile('blur_bg.jpg')

except Exception as e:
    print 'non load OpenCV'

#  load OpenEXR
try:
    import OpenEXR
    import other_imath
    import matplotlib

    assert os.path.isfile('Rec709.exr')
    openexr_test = OpenEXR.InputFile('Rec709.exr')
    o_exr_dict = openexr_test.header()
    out = o_exr_dict['displayWindow'].max
    assert out.x == 609
    assert out.y == 405
    # 4 number - PIZ_COMPRESSION '''PIZ_COMPRESSION = 4'''
    assert 4 == other_imath.Compression.PIZ_COMPRESSION
    assert other_imath.Compression(
        other_imath.Compression.PIZ_COMPRESSION) == o_exr_dict['compression']

    # 8 number - DWAA_COMPRESSION
    assert os.path.isfile('exr_test.exr')
    openexr_test2 = OpenEXR.InputFile('exr_test.exr')
    assert other_imath.Compression.DWAA_COMPRESSION == 8
    assert other_imath.Compression(
        other_imath.Compression.DWAA_COMPRESSION) == openexr_test2.header()['compression']

    # p_type = other_imath.PixelType(other_imath.PixelType.FLOAT)
    # dw = openexr_test2.header()['dataWindow']
    # exr_size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    # print exr_size, openexr_test2.header()['channels'].keys()[0]
    # redstr = openexr_test2.channel('R', p_type)

    # rexr = numpy.fromstring(redstr, dtype=float)

    # print rexr

except Exception as e:
    print 'non load OpenEXR'

AMG Scatter utils
=================

**amg_scatter_utils** is a set of methods for getting vector data from Maya (MASH/XGen) and calculate transformation matrix (M44f) based on them. Implemented as a package for python 2.7.


amg_scatter_utils features include:

* ocmash() - method to work with Maya/MASH
* ocpartio() - method to work with Maya/XGen (*.begeo)
* M44f() - method for testing transformation matrix.


Installation instructions for amg_scatter_utils
-----------------------------------------------

Before amg_scatter_utils can be built, you will need to satisfy its external
dependencies:

* OpenEXR (2.3.0) for ilmbase (www.openexr.com)
* Partio - library for particle IO and manipulation (www.partio.us)
* zlib - (www.zlib.net).


#### Building from Git

You can download the latest release from https://github.com/animagrad/rnd/tree/master/amg_scatter_utils.

or 

    git clone https://github.com/animagrad/rnd/tree/master/amg_scatter_utils [<source root>]


Edit contents of "install-base" according to your PYTHONPATH

    setup.cfg

    [install]
    install-base=$HOME/projects/rnd/amg_scatter_utils
    install-purelib=lib
    install-platlib=.
    install-scripts=scripts
    install-headers=python/include
    install-data=data

Edit contents of "include_dir", "lib_partio" according to your include and lib path

    setup.py

    include_dir = '//bstorage/rep/set/include'
    lib_partio = '//bstorage/rep/set/libs/lib_' + sys_name

For Unix like operating systems (gcc 4.8.5):

    cd <source root>
    python setup.py build
    python setup.py install
    python setup.py test

For Windows (VS 2015/2014):

Add the path to compiled libraries (OpenEXR, Partio, etc.) in environment variable 'PATH'.

    cd <source root>
    SET VS90COMNTOOLS=%VS140COMNTOOLS%
    python setup.py build
    python setup.py install
    python setup.py test
    

A Simple Example
----------------

get data from *.bgeo

    import amg_scatter_utils
    mtx = amg_scatter_utils.ocpartio(test.bgeo)

Returns dictionary (dict) where keys (key) are object indices (int), in values, we getting the transformation matrices (m44f) in the form of a flat array. {(int) index: [m44f FloatArray]}


get fata from Maya/MASH

    import MASH.api as mapi
    import maya.OpenMaya as om
    import amg_scatter_utils

    mash_node = om.MObject()
    sel.getDependNode(0, mash_node)
    mash_node_fn = om.MFnDependencyNode(mash_node)
    points_attribute = mash_node_fn.attribute('inputPoints')
    points_plug = om.MPlug(mash_node, points_attribute)
    handle_data = points_plug.asMDataHandle().data()
    input_points_data = om.MFnArrayAttrsData(handle_data)

    mtx = amg_scatter_utils.ocmash(input_points_data)

We get same dictionary as in the first example.
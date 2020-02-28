Symmetry check
=================

Symmetry check - maya/python module.
---------------------

Finding asymmetric polygons relative to X axis

<!-- export LD_LIBRARY_PATH=/boost/boost-1.67_gcc-4.8.5/lib -->

export LD_LIBRARY_PATH=/opt/sandbox/boost-1.67_gcc-4.8.5/lib


	import sys
	module_path = 'symmetry_check-v0.0.1'
	if module_path not in sys.path:
	    sys.path.append(module_path)
	    
	import symmetry
	reload(symmetry)
	symmetry.maya_main()


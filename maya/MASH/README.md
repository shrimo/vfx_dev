Write alembic
=================

Write alembic - maya/XGen/MASH/python module.
---------------------

Read *.bgeo file sequence - write *.abc file

export LD_LIBRARY_PATH=/bstorage/rep/set/boost/boost-1.67_gcc-4.8.5/lib

export LD_LIBRARY_PATH=/opt/sandbox/boost-1.67_gcc-4.8.5/lib

/home/v.lavrentev/projects/cpp/partio/bgeo/02


	import sys
	module_path = '/home/v.lavrentev/projects/rnd/write_alembic'
	if module_path not in sys.path:
	    sys.path.append(module_path)
	    
	import write_abc
	reload(write_abc)
	write_abc.abc_main()

	import sys
	module_path = '/home/v.lavrentev/project/rnd/write_alembic'
	if module_path not in sys.path:
		sys.path.append(module_path)
		
	import maya_mash
	reload(maya_mash)
	maya_mash.main()

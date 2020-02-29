from distutils.cmd import Command
from distutils.core import setup, Extension
import platform

sys_name = platform.system().lower()
include_dir = '/usr/local/include'
# lib_partio = '//usr/local/lib64' + sys_name

class TestCommand(Command):
	user_options = []
	def initialize_options(self):
		pass
	def finalize_options(self):
		pass
	def run(self):
		print 'test - amg_scatter_utils'
		import amg_scatter_utils
		import os
		file_path = 'test_classic.bgeo'
		if os.path.exists(file_path):        
			mtx = amg_scatter_utils.ocpartio(file_path)
			print "- Python -"
			for i in mtx:
				print "\n", i," -key- \n", mtx[i]
		else:
			print file_path, ' -> no file'

if sys_name == 'linux':
	print 'Operating system: Linux'
	module_amg = Extension(		
		name='amg_scatter_utils',
		sources=['src/amg_scatter_utils.cpp'],
		include_dirs=[include_dir],
		extra_compile_args=['--std=c++11'],
		extra_link_args=['--std=c++11'])
elif sys_name == 'windows':
	print 'Operating system: Windows'
	module_amg = Extension(
		name='amg_scatter_utils',
		sources=['src/amg_scatter_utils.cpp'],
		include_dirs=[include_dir],
		libraries=['Iex-2_3', 'Half-2_3', 'Imath-2_3', 'IlmImf-2_3', 'zlib', 'partio'])
else:
	print 'Operating system: Unknown'

setup(
    name='amg_scatter_utils',
    version='1.0',
    description='amg_scatter_utils package. Get data and matrix calculation from Maya/MASH/Xgen',
    ext_modules=[module_amg],
	cmdclass={'test': TestCommand})

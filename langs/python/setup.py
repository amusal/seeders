'''
How to use:
	1. modified py_modules and other configures;
	2. cmd/shell=> python setup.py sdist
	3. cmd/shell=> python setup.py install
Publish to pypi:
	1. register in http://pypi.python.org;
	2. cmd/shell=> python setup.py register
	note: step 2 only need once, if registered yet, ignore this step
	3. cmd/shell=> python setup.py sdist upload
'''

from distutils.core import setup

setup(
	name			= 'app-name',
	version			= '1.0.0',
	py_modules		= ['module_name'],
	author			= 'johnson',
	author_email	= 'johnson@tom.com',
	url				= 'http://github.com/amusal',
	description		= 'app desc'
	)
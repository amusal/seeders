'''
Put this file into directory PYTHON_HOME/lib/site-packages/

Invoke sys.getdefaultencoding(), we can get the right encoding.
'''
import sys
import platform

if platform.system() == 'Windows':
    sys.setdefaultencoding('gbk')
else:
    sys.setdefaultencoding('utf-8')
from distutils.core import setup
import py2exe

setup(
    windows=[{'script': 'hufsgrade.py'}],
    options={
            'py2exe':
            {
                    'includes': ['PyQt4.QtGui', 'PyQt4.QtCore'],
            }
    }
)
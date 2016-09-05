from distutils.core import setup
import py2exe
import requests.certs

setup(
    windows=[{'script': 'hufsgrade.py'}],
    options={
            'py2exe':
            {
                    'includes': ['PyQt4.QtGui', 'PyQt4.QtCore', 'requests', 're', 'time', 'bs4', 'sip'],
            }
    }
    #data_files=['cacert.pem']
)
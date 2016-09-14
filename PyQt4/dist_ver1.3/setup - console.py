from distutils.core import setup
import py2exe
import requests.certs

Mydata_files = [('images', ['C:/Users/hufs/Downloads/download/lawjmc/hufsgrade/hufslogo.png'])]

setup(
    console = [
        {
            "script": "hufsgrade_ver1.0.py",
            "icon_resources": [(0, "hufslogo.png.ico")]
        }
    ],
    options={
            'py2exe':
            {
                    'includes': ['PyQt4.QtGui', 'PyQt4.QtCore', 'requests', 're', 'time', 'bs4', 'sip', 'os'],
            }
    },
    data_files= Mydata_files
)

from distutils.core import setup
import py2exe
import requests.certs

setup(
    console=['hufsgrade_cacert.py'],
    data_files=['cacert.pem']
)
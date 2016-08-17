import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic

import requests
from bs4 import BeautifulSoup
import re

form_class = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

# 진도체크: https://wikidocs.net/5227

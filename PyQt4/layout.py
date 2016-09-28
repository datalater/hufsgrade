import sys
from PyQt4 import QtGui

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()        
        self.initUI()
        
    def initUI(self):
        
        okButton = QtGui.QPushButton("OK")
        cancelButton = QtGui.QPushButton("Cancel")
        
        okButton2 = QtGui.QPushButton("OK2")
        cancelButton2 = QtGui.QPushButton("Cancel2")

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(okButton2)
        hbox2.addWidget(cancelButton2)

        hbox3 = QtGui.QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addLayout(hbox)
        hbox3.addLayout(hbox2)
        
        self.setLayout(hbox3)    
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

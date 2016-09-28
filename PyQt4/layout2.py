import sys
from PyQt4 import QtGui

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()        
        self.initUI()
        
    def initUI(self):
        
        btn1 = QtGui.QPushButton("1")
        btn2 = QtGui.QPushButton("2")
        btn3 = QtGui.QPushButton("3")
        btn4 = QtGui.QPushButton("4")

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(btn1)
        hbox1.addStretch(1)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(btn2)
        hbox2.addStretch(1)

        hbox_total = QtGui.QHBoxLayout()
        hbox_total.addLayout(hbox1)
        hbox_total.addLayout(hbox2)

        self.setLayout(hbox_total)
        
        '''
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(2)
        hbox2.addWidget(okButton2)
        hbox2.addWidget(cancelButton2)

        hbox3 = QtGui.QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addLayout(hbox)
        hbox3.addLayout(hbox2)
        
        self.setLayout(hbox3)
        '''
        
        self.setGeometry(300, 300, 500, 350)
        self.setWindowTitle('Buttons')    
        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

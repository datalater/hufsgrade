import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic

import requests
from bs4 import BeautifulSoup
import re

head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
login_url = "https://webs.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp"
main_page = "http://webs.hufs.ac.kr:8989/src08/jsp/main.jsp?"
studentinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/stuinfo_10/STUINFO1000C_myinfo.jsp"
credits_url = "http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_Top.jsp?tab_lang=K"

form_class = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.login)

    def login(self):
        self.current_session = requests.session()
        params = {'user_id': self.lineEdit.text(),'password': self.lineEdit_2.text(),'gubun': 'o','reurl': '','SSL_Login': 1}

        self.current_session.post(login_url, data=params, headers=head)
        self.current_session.get(main_page, headers=head)

        self.studentinfo = self.current_session.get(studentinfo_url, headers=head)
        html = BeautifulSoup(self.studentinfo.text, "html.parser")

        student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
        student_major = student_college.next_element.next_element.next_element.next_element.string
        student_id= html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
        student_name = html.find(string=re.compile('성명')).parent.parent.next_sibling.next_element.next_element.next_element.next_sibling.next_sibling.string
        student_name = student_name.replace("\r\n\t\t\t\t","")

        # 크롤링 테스트
        self.label_3.setText(student_college)
        print(student_college)

        # 상태bar
        self.label_4.setText("로그인 성공하였습니다.")

        # 위젯 delete 코드 쓰기
        self.label.deleteLater()
        self.label = None
        self.label_2.deleteLater()
        self.label = None
        self.lineEdit.deleteLater()
        self.label = None
        self.lineEdit_2.deleteLater()
        self.label = None
        self.pushButton.deleteLater()
        self.label = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

# 진도체크: https://wikidocs.net/5236

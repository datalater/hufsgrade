# 진도체크(things to do)
# 1. 로그아웃 버튼(Home버튼) 만들기
# 2. 첫 화면 디자인 확실히 정하기
# 3. 로그인 기능에서 로그인이 안 되면 오류 메시지 보여주기

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
credits_list_url = "http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_List.jsp?tab_lang=K"


form_class = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect(self.pushButton, SIGNAL("clicked()"), self.login)
        
        self.label_4.setText("한국외국대학교 종합정보시스템 ID와 PWD를 입력해주세요.")

        #-------------------------위젯 하이드--------------------------#
        self.line_2.hide()
        self.label_3.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.tableWidget.hide()

    def login(self):
        self.current_session = requests.session()
        params = {'user_id': self.lineEdit.text(),'password': self.lineEdit_2.text(),'gubun': 'o','reurl': '','SSL_Login': 1}
        
        self.current_session.post(login_url, data=params, headers=head)
        
        #-------------------------학생정보--------------------------#
        self.current_session.get(main_page, headers=head)

        self.studentinfo = self.current_session.get(studentinfo_url, headers=head)
        html = BeautifulSoup(self.studentinfo.text, "html.parser")

        student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
        student_major = student_college.next_element.next_element.next_element.next_element.string
        student_id= html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
        student_name = html.find(string=re.compile('성명')).parent.parent.next_sibling.next_element.next_element.next_element.next_sibling.next_sibling.string
        student_name = student_name.replace("\r\n\t\t\t\t","")
        student_name_ko = html.find(string=re.compile('성명')).parent.next_sibling.next_sibling.next_sibling.next_sibling.string
        
        #-------------------------성적정보(영역별취득학점)--------------------------#

        self.graduateinfo=self.current_session.get(credits_url,headers=head)
        html = BeautifulSoup(self.graduateinfo.text, "html.parser")
        
        major_state = ""
        if html.find(string=re.compile('\[이중전공\]')) is not None:
            major_state ="이중전공"
        elif html.find(string=re.compile('전공심화')) is not None:
            major_state = "전공심화(부전공)"
        else:
            major_state = "not yet decided"

        grade_data = [i.string for i in html.find("tr",class_="table_w").find_all("td")]
        credits_completed = grade_data[1:-2]
        grade_per_average = grade_data[-2:-1]
                        
        graduateinfo = credits_completed + grade_per_average
        
        #2015~학번(사범대 제외)
        #dual_major_required = [54, 42, 0, 6, 26, 0, 0, 6, 134,4.5]
        #minor_required = [70, 0, 21, 6, 26, 0, 0, 11, 134,4.5]
      
        #2007~2014학번(사범대 제외)
        dual_major_required = [54, 54, 0, 4, 22, 0, 0, 0, 134, 4.5]
        minor_required = [75, 0, 0, 4, 22, 21, 0, 12, 134, 4.5]
        dual_major_required = list(map(str, dual_major_required))
        minor_required = list(map(str, minor_required))

        #-------------------------성적정보(전공평점)--------------------------#

        self.creditsinfo=self.current_session.get(credits_list_url,headers=head)
        html = BeautifulSoup(self.creditsinfo.text, "html.parser")

        grade_dic = {'A+':4.5, 'A0':4.0, 'B+':3.5, 'B0':3.0, 'C+':2.5, 'C0':2.0, 'D+':1.5, 'D0':1.0, 'F':0}

        # 전공 평점 구하기 시작
        first_major_credit = [] # credit: 학점(e.g. 3)
        first_major_grade = [] # grade: 등급(e.g. A+)
        first_major_grade_float = [] # grade_float: 등급 환산 점수(e.g. A+ -> 4.5)
        first_major_multiply = []
        
        for td in html.find_all("tr",class_="table_w"):
            for td_first_major in td.find_all(string=re.compile('1전공|이중')):
                for td_credits in td_first_major.parent.next_sibling.next_sibling:
                    first_major_credit.append(float(td_credits))
                for td_grades in td_first_major.parent.next_sibling.next_sibling.next_sibling.next_sibling:
                    first_major_grade.append(td_grades)

        # 등급 점수로 환산하기(e.g. A+ -> 4.5)
        for element in first_major_grade:
            first_major_grade_float.append(grade_dic[element])
            
        # 학점 곱하기 등급
        for i in range(len(first_major_credit)):
            first_major_multiply.append(first_major_credit[i] * first_major_grade_float[i])

        # 전공 평점 구하기 끝
        first_major_gpa = round(sum(first_major_multiply)/sum(first_major_credit),2)
        
        
        
        #-------------------------학생정보 나타내기--------------------------#
        self.label_3.setText(student_id)
        self.label_6.setText("영역별 취득학점: "+major_state+" 기준")
        self.label_5.setText(student_name_ko+"("+student_name+")"+"님, 반갑습니다.")
        
        
        #-------------------------성적정보 테이블 위젯에 나타내기--------------------------#
        if major_state == "이중전공": 
            for i in range(len(dual_major_required)):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
                item.setText(dual_major_required[i])
                self.tableWidget.setItem(0, i, item)
                
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
                item.setText(graduateinfo[i])
                self.tableWidget.setItem(1, i, item)
                if i <9:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
                    brush = QBrush(QColor(220, 255, 217))
                    brush.setStyle(Qt.SolidPattern)
                    item.setBackground(brush)
                    item.setText(str(int(dual_major_required[i])-int(graduateinfo[i])))
                    self.tableWidget.setItem(2, i, item)
        elif major_state == "전공심화(부전공)":
            for i in range(len(minor_required)):
                self.tableWidget.setItem(0, i, QTableWidgetItem(minor_required[i]))
                self.tableWidget.setItem(1, i, QTableWidgetItem(graduateinfo[i]))
                if i <9:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
                    brush = QBrush(QColor(220, 255, 217))
                    brush.setStyle(Qt.SolidPattern)
                    item.setBackground(brush)
                    self.tableWidget.setItem(2, i, QTableWidgetItem(str(int(minor_required[i])-int(graduateinfo[i]))))                    
        else:
            for i in range(len(dual_major_required)):
                self.tableWidget.setItem(1, i, QTableWidgetItem(graduateinfo[i]))

        self.label_8.setText(str(first_major_gpa)+")")
                
        #-----------------------------------------------------------------------------------#

        # 상태bar
        self.label_4.setText("로그인 성공하였습니다.")

        #-------------------------로그인 위젯 delete--------------------------#
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

        #-------------------------위젯 show--------------------------#
        self.line.hide()
        self.line_2.show()
        self.label_3.show()
        self.label_5.show()
        self.label_6.show()
        self.label_7.show()
        self.label_8.show()
        self.tableWidget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

# 진도체크: https://wikidocs.net/5236

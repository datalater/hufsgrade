import os
import sys
from PyQt4 import QtGui, QtCore
import logging

import requests
from bs4 import BeautifulSoup
import re
import time
#from os.path import join, abspath

head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
login_url = "https://webs.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp"
main_page = "http://webs.hufs.ac.kr:8989/src08/jsp/main.jsp?"
studentinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/stuinfo_10/STUINFO1000C_myinfo.jsp"
credits_url = "http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_Top.jsp?tab_lang=K"
credits_list_url = "http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_List.jsp?tab_lang=K"

#requests.utils.DEFAULT_CA_BUNDLE_PATH = join(abspath('.'), 'cacert.pem')
cafile = 'cacert.pem'
hufsfile = 'hufslogo.png'

full_size = [660, 500]

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, full_size[0], full_size[1])
        self.setWindowTitle("HUFSGrade_ver1.5")
        self.setWindowIcon(QtGui.QIcon(hufsfile))

        # start-menubar
        extractAction = QtGui.QAction("&종료하기", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.triggered.connect(self.close_application)

        helpAction = QtGui.QAction("&프로그램 정보", self)
        helpAction.setShortcut("Ctrl+I")
        helpAction.triggered.connect(self.info_application)
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(helpAction)
        # end-menubar
        
        self.label = QtGui.QLabel("ID", self)
        self.label.setGeometry(200, 20, 90, 20)
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setGeometry(300, 20, 150, 20)
        self.lineEdit.returnPressed.connect(self.login)
        
        self.label_2 = QtGui.QLabel("PASSWORD", self)
        self.label_2.setGeometry(200, 50, 90, 20)
        self.lineEdit_2 = QtGui.QLineEdit(self)
        self.lineEdit_2.setGeometry(300, 50, 150, 20)
        self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_2.returnPressed.connect(self.login)
        
        self.pushButton = QtGui.QPushButton("로그인", self)
        self.pushButton.setGeometry(200, 80, 250, 28)
        self.pushButton.clicked.connect(self.login)
        self.pushButton.setAutoDefault(True)
        #self.pushButton.returnPressed.connect(self.login)
        
        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(430, 475, 220, 20)
        
        self.pushButton_2 = QtGui.QPushButton("뒤로가기", self)
        self.pushButton_2.setGeometry(552, 440, 80, 28)
        self.pushButton_2.clicked.connect(self.goback)
        
        self.label_3 = QtGui.QLabel("학번", self)
        self.label_3.setGeometry(10, 10, 280, 20)
        
        self.label_5 = QtGui.QLabel("이름", self)
        self.label_5.setGeometry(370, 10, 280, 20)
        self.label_5.setAlignment(QtCore.Qt.AlignRight)
        
        self.line = QtGui.QFrame(self)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setGeometry(0, 95, 660, 60)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        
        self.line_2 = QtGui.QFrame(self)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setGeometry(0, 25, 660, 20)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        
        self.label_6 = QtGui.QLabel("영역별 취득 학점", self)
        self.label_6.setGeometry(20, 65, 240, 20)
        
        self.label_7 = QtGui.QLabel("(전공평점: )", self)
        self.label_7.setGeometry(535, 65, 120, 20)
                
        self.label_4 = QtGui.QLabel("한국외국대학교 종합정보시스템 ID와 PWD를 입력해주세요.", self)
        self.label_4.setGeometry(5, 475, 500, 20)
        
        self.tableWidget = QtGui.QTableWidget(self)
        self.tableWidget.setGeometry(20, 90, 615, 130)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(3)
        
        # table cell[start]
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 4, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 5, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 6, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 7, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 8, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(0, 9, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 4, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 5, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 6, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 7, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 8, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(1, 9, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(2, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(2, 1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(2, 2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(2, 3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(2, 4, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(2, 5, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(2, 6, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(2, 7, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(2, 8, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.tableWidget.setItem(2, 9, item)
        
        self.tableWidget.horizontalHeaderItem(0).setText("1전공")
        self.tableWidget.horizontalHeaderItem(1).setText("이중")
        self.tableWidget.horizontalHeaderItem(2).setText("2전공")
        self.tableWidget.horizontalHeaderItem(3).setText("실외")
        self.tableWidget.horizontalHeaderItem(4).setText("교양")
        self.tableWidget.horizontalHeaderItem(5).setText("부전공")
        self.tableWidget.horizontalHeaderItem(6).setText("교직")
        self.tableWidget.horizontalHeaderItem(7).setText("자선")
        self.tableWidget.horizontalHeaderItem(8).setText("총취득")
        self.tableWidget.horizontalHeaderItem(9).setText("총평점")
        
        self.tableWidget.verticalHeaderItem(0).setText("전체")
        self.tableWidget.verticalHeaderItem(1).setText("취득")
        self.tableWidget.verticalHeaderItem(2).setText("차분")
        
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(57)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(35)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        
        
        # table cell[end]
        
        
        self.show()
        
        
        self.line_2.hide()
        self.label_3.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.tableWidget.hide()
        self.pushButton_2.hide()
        
        
    def login(self):
    
        self.current_session = requests.session()
        params = {'user_id': self.lineEdit.text(),'password': self.lineEdit_2.text(),'gubun': 'o','reurl': '','SSL_Login': 1}
        
        self.current_session.post(login_url, data=params, headers=head, verify=cafile)
        
        #-------------------------학생정보--------------------------#
        self.current_session.get(main_page, headers=head, verify=cafile)

        self.studentinfo = self.current_session.get(studentinfo_url, headers=head, verify=cafile)
        html = BeautifulSoup(self.studentinfo.text, "html.parser")

        student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
        try:
            student_major = student_college.next_element.next_element.next_element.next_element.string
            self.completed = 0
        
            while self.completed < 100:
                self.completed += 0.00008
                self.progress.setValue(self.completed)
        except AttributeError:
            self.label_4.setText("잘못된 로그인입니다.")
            
        #student_id= html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
        student_id = self.lineEdit.text()
        student_name = html.find(string=re.compile('성명')).parent.parent.next_sibling.next_element.next_element.next_element.next_sibling.next_sibling.string
        student_name = student_name.replace("\r\n\t\t\t\t","")
        student_name_ko = html.find(string=re.compile('성명')).parent.next_sibling.next_sibling.next_sibling.next_sibling.string

        
        # 입학연도 
        student_id_year = int(str(student_id)[:4])
        
        
        #-------------------------성적정보(영역별취득학점)--------------------------#

        self.graduateinfo=self.current_session.get(credits_url,headers=head, verify=cafile)
        html = BeautifulSoup(self.graduateinfo.text, "html.parser")
        
        # 이중전공자 전공심화자 구분 및 각 전공 과목 parsing
        major_state = ""
        if html.find(string=re.compile('\[이중전공\]')) is not None:
            major_state ="이중전공"
            student_other_major = html.find(string=re.compile('\[이중전공\]')).next_element
            student_other_major = student_other_major.replace(u'\xa0', u' ').replace("(","").replace(" ","")
            student_other_major = "이중: " + student_other_major
        elif html.find(string=re.compile('전공심화')) is not None:
            major_state = "전공심화(부전공)"
            student_other_major = html.find(string=re.compile('전공심화')).next_element
            student_other_major = student_other_major.replace(u'\xa0', u' ').replace("(","").replace(" ","")
            student_other_major = "부:" + student_other_major
        else:
            major_state = "not yet decided"
        
        # 1전공 parsing
        student_first_major = html.find(string=re.compile('\[1전공\]')).next_element
        student_first_major = student_first_major.replace(u'\xa0', u' ').replace("(","").replace(" ","")
        
        grade_data = [i.string for i in html.find("tr",class_="table_w").find_all("td")]
        credits_completed = grade_data[1:-2]
        grade_per_average = grade_data[-2:]
                        
        graduateinfo = credits_completed + grade_per_average
        
        #2015~학번(사범대 제외)
        dual_major_required_15 = [54, 42, 0, 6, 26, 0, 0, 6, 134, 4.5]
        minor_required_15         = [70, 0, 21, 6, 26, 0, 0, 11, 134, 4.5]
        dual_major_required_15 = list(map(str, dual_major_required_15))
        minor_required_15         = list(map(str, minor_required_15))
        
        #2007~2014학번(사범대 제외)
        dual_major_required  = [54, 54, 0, 4, 22, 0, 0, 0, 134, 4.5]
        minor_required          = [75, 0, 0, 4, 22, 21, 0, 12, 134, 4.5]
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
        self.label_3.setText(student_id + " " + student_first_major + "(" + student_other_major + ")")
        self.label_6.setText("영역별 취득학점: "+major_state+" 기준")
        self.label_5.setText(student_name_ko+"("+student_name+")"+"님, 반갑습니다.")
        
        # 상태bar
        self.label_4.setText("졸업 심사 시 전체를 넘는 취득학점은 자선으로 처리됩니다.")
        
        #-------------------------성적정보 테이블 위젯에 나타내기--------------------------#
                
        if student_id_year >= 2007 and student_id_year < 2015:   
            
            if major_state == "이중전공": 
                for i in range(len(dual_major_required)):
                    item = QtGui.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                    item.setText(dual_major_required[i])
                    self.tableWidget.setItem(0, i, item)
                    
                    item = QtGui.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                    item.setText(graduateinfo[i])
                    self.tableWidget.setItem(1, i, item)
                    if i <9:
                        item = QtGui.QTableWidgetItem()
                        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
                        brush.setStyle(QtCore.Qt.SolidPattern)
                        item.setBackground(brush)
                        item.setText(str(int(dual_major_required[i])-int(graduateinfo[i])))
                        self.tableWidget.setItem(2, i, item)
            elif major_state == "전공심화(부전공)":
                for i in range(len(minor_required)):
                    item = QtGui.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                    item.setText(minor_required[i])
                    self.tableWidget.setItem(0, i, item)
                    
                    item = QtGui.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                    item.setText(graduateinfo[i])
                    self.tableWidget.setItem(1, i, item)
                    if i <9:
                        item = QtGui.QTableWidgetItem()
                        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
                        brush.setStyle(QtCore.Qt.SolidPattern)
                        item.setBackground(brush)
                        item.setText(str(int(minor_required[i])-int(graduateinfo[i])))
                        self.tableWidget.setItem(2, i, item)                    
            else:
                for i in range(len(dual_major_required)):
                    self.tableWidget.setItem(1, i, QtGui.QTableWidgetItem(graduateinfo[i]))
                    
        elif student_id_year >= 2015:
            
            self.tableWidget.horizontalHeaderItem(3).setText("교외")
            
            if major_state == "이중전공": 
                for i in range(len(dual_major_required)):
                    item = QtGui.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                    item.setText(dual_major_required_15[i])
                    self.tableWidget.setItem(0, i, item)
                    
                    item = QtGui.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                    item.setText(graduateinfo[i])
                    self.tableWidget.setItem(1, i, item)
                    if i <9:
                        item = QtGui.QTableWidgetItem()
                        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
                        brush.setStyle(QtCore.Qt.SolidPattern)
                        item.setBackground(brush)
                        item.setText(str(int(dual_major_required_15[i])-int(graduateinfo[i])))
                        self.tableWidget.setItem(2, i, item)
            elif major_state == "전공심화(부전공)":
                for i in range(len(minor_required)):
                    item = QtGui.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                    item.setText(minor_required_15[i])
                    self.tableWidget.setItem(0, i, item)
                    
                    item = QtGui.QTableWidgetItem()
                    item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                    item.setText(graduateinfo[i])
                    self.tableWidget.setItem(1, i, item)
                    if i <9:
                        item = QtGui.QTableWidgetItem()
                        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                        brush = QtGui.QBrush(QtGui.QColor(220, 255, 217))
                        brush.setStyle(QtCore.Qt.SolidPattern)
                        item.setBackground(brush)
                        item.setText(str(int(minor_required_15[i])-int(graduateinfo[i])))
                        self.tableWidget.setItem(2, i, item)                    
            else:
                for i in range(len(dual_major_required)):
                    self.tableWidget.setItem(1, i, QtGui.QTableWidgetItem(graduateinfo[i]))
            
        else:
            for i in range(len(dual_major_required)):
                
                item = QtGui.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
                item.setText(graduateinfo[i])
                self.tableWidget.setItem(1, i, item)
            self.label_4.setText("07년도 이전 입학 학번에 대해서는 필수학점을 제공하지 않습니다.")
            
        self.label_7.setText("(전공평점: "+str(first_major_gpa)+")")
                
        #-----------------------------------------------------------------------------------#

        
        #-------------------------로그인 위젯 hide--------------------------#
        self.label.hide()
        self.label_2.hide()
        self.lineEdit.hide()
        self.lineEdit_2.hide()
        self.pushButton.hide()
        self.line.hide()
        self.progress.hide()
        

        #-------------------------학생/성적정보 위젯 show--------------------------#
        self.line_2.show()
        self.label_3.show()
        self.label_5.show()
        self.label_6.show()
        self.label_7.show()
        self.tableWidget.show()
        self.pushButton_2.show()
        
    def goback(self):
        self.progress.reset()
        #-------------------------학생/성적정보 위젯 hide--------------------------#
        self.line_2.hide()
        self.label_3.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.tableWidget.hide()
        self.pushButton_2.hide()

        #-------------------------로그인 위젯 show--------------------------#
        self.label.show()
        self.label_2.show()
        self.lineEdit.show()
        self.lineEdit_2.show()
        self.pushButton.show()
        self.line.show()
        self.progress.show()
        
        self.label_4.setText("한국외국대학교 종합정보시스템 ID와 PWD를 입력해주세요")

    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, 'Message',
            "종료하시겠습니까?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def close_application(self):
        sys.exit()

    def info_application(self):
        
        info_msg = QtGui.QMessageBox()
        #info_msg.setIcon(QtGui.QMessageBox.Information)
        info_msg.setText(
            """
버전: 1.5
개발자: 조민철
문의: the7mincheol@naver.com
다운로드: http://bit.ly/2dfS8GZ
""")
        info_msg.setWindowTitle("프로그램 정보")
        #info_msg.setDetailedText("The details are as follows:")

        info_msg.exec_()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
    logger = logging.getLogger('my-logger')
    logger.propagate = False
    sys.stderr = sys.stdout
    sys.tracebacklimit = 0
    sys.stderr = sys.stdout = os.devnull
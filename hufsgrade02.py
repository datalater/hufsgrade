import requests
from bs4 import BeautifulSoup
import getpass

from kivy.app import App
from kivy.uix.widget import Widget
import re
import time

#headers=head의 역할
#params vs data=params

head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
login_url = "https://webs.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp"
main_page = "http://webs.hufs.ac.kr:8989/src08/jsp/main.jsp?"
studentinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/stuinfo_10/STUINFO1000C_myinfo.jsp"
gradeinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_Top.jsp?tab_lang=K"

class parse_score():
    def __init__(self):
        self.yourid = input("아이디: ")
        self.yourpwd = getpass.getpass("비밀번호: ")

    def login(self):
        self.current_session = requests.session()

        params={
            'user_id':self.yourid,
            'password':self.yourpwd,
            'gubun':'o',
            'reurl':'',
            'SSL_Login':1
            }

        self.current_session.post(login_url,data=params,headers=head)
        self.current_session.get(main_page,headers=head)

    def studentinfo(self):
        self.studentinfo=self.current_session.get(studentinfo_url,headers=head)
        html = BeautifulSoup(self.studentinfo.text, "html.parser")

        #print(html.text)

        student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
        student_major = student_college.next_element.next_element.next_element.next_element.string
        student_id= html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
        student_name = html.find(string=re.compile('성명')).parent.parent.next_sibling.next_element.next_element.next_element.next_sibling.next_sibling.string
        student_name = student_name.replace("\r\n\t\t\t\t","")
        print(student_college)
        print(student_major)
        print(student_id)
        print(student_name)


        self.gradeinfo=self.current_session.get(gradeinfo_url,headers=head)
        html = BeautifulSoup(self.gradeinfo.text, "html.parser")
        
        major_state = ""
        if html.find(string=re.compile('이중전공')) is not None:
            major_state ="Dual major"
        elif html.find(string=re.compile('부전공')) is not None:
            major_state = "Minor"
        else:
            major_state = "not yet decided"
        print(major_state)
        
        grade_data = [i.string for i in html.find("tr",class_="table_w").find_all("td")]
        credits_completed = grade_data[1:-2]
        grade_per_average = grade_data[-2:-1]
        credits_completed = list(map(int, credits_completed))
        grade_per_average = list(map(float, grade_per_average))
        print(credits_completed)
        print(grade_per_average)

        #2015~학번(사범대 제외)
        #dual_major_required = [54, 42, 0, 6, 26, 0, 0, 6, 134]
        #minor_required = [70, 0, 21, 6, 26, 0, 0, 11, 134]
      
        #2007~2014학번(사범대 제외)
        dual_major_required = [54, 54, 0, 4, 22, 0, 0, 0, 134]
        minor_required = [75, 0, 21, 4, 22, 0, 0, 12, 134]
        
        

        


# 소속대학: student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
# 소속학과: student_major = student_college.next_element.next_element.next_element.next_element.string
# 학번: student_id = html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
# 성명: student_name = html.find(string=re.compile('성명')).parent.next_sibling.next_sibling.next_sibling.next_sibling.string
# 성명: student_name = student_name.replace("\r\n\t\t\t\t","")


        


if __name__ == '__main__':
    p = parse_score()
    p.login()
    p.studentinfo()
    
    

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button
from kivy.factory import Factory

import requests
from bs4 import BeautifulSoup
import re



head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
login_url = "https://webs.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp"
main_page = "http://webs.hufs.ac.kr:8989/src08/jsp/main.jsp?"
studentinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/stuinfo_10/STUINFO1000C_myinfo.jsp"
credits_to_graduate_url = "http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_Top.jsp?tab_lang=K"

class HufsGradeRoot(BoxLayout):
    def grade_analysis(self):
        self.clear_widgets()
        grade_anlysis = Factory.Grade_Analysis()
        self.add_widget(grade_analysis)
        
    def show_login_form(self): # graduate의 back버튼(to Home)
        self.clear_widgets()
        self.add_widget(LoginForm())
        

class LoginForm(BoxLayout):    
    id_input = ObjectProperty()
    pwd_input = ObjectProperty()
    studentinfo_results = ObjectProperty()
    

    def login(self):
        self.current_session = requests.session()

        params={
            'user_id': self.id_input.text,
            'password': self.pwd_input.text,
            'gubun': 'o',
            'reurl': '',
            'SSL_Login': 1
            }

        self.current_session.post(login_url,data=params,headers=head)
        self.current_session.get(main_page,headers=head)
                
        print("user id is '{}',\nuser pwd is '{}'.".format(self.id_input.text, self.pwd_input.text))
        
        self.studentinfo=self.current_session.get(studentinfo_url,headers=head)
        html = BeautifulSoup(self.studentinfo.text, "html.parser")
        
        student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
        student_major = student_college.next_element.next_element.next_element.next_element.string
        student_id= html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
        student_name = html.find(string=re.compile('성명')).parent.parent.next_sibling.next_element.next_element.next_element.next_sibling.next_sibling.string
        student_name = student_name.replace("\r\n\t\t\t\t","")
        
        studentinfo = [student_college, student_major, student_id, student_name]
        self.studentinfo_results.item_strings = studentinfo
        self.studentinfo_results.adapter.data.clear()
        self.studentinfo_results.adapter.data.extend(studentinfo)
        self.studentinfo_results._trigger_reset_populate()

# 소속(ResultSet): html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.stripped_strings
# 학번: html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
# 성명: html.find(string=re.compile('성명')).parent.next_sibling.next_sibling.next_sibling.next_sibling.string

    def credits_to_graduate(self):
        self.current_session = requests.session()

        params={
            'user_id': self.id_input.text,
            'password': self.pwd_input.text,
            'gubun': 'o',
            'reurl': '',
            'SSL_Login': 1
            }

        self.current_session.post(login_url,data=params,headers=head)
        self.current_session.get(main_page,headers=head)
                
        print("user id is '{}',\nuser pwd is '{}'.".format(self.id_input.text, self.pwd_input.text))
        
        self.credits_to_graduate=self.current_session.get(credits_to_graduate_url,headers=head)
        html = BeautifulSoup(self.credits_to_graduate.text, "html.parser")
        
        major_state = ""
        if html.find(string=re.compile('이중전공')) is not None:
            major_state ="dual major"
        elif html.find(string=re.compile('부전공')) is not None:
            major_state = "minor"
        else:
            major_state = "not yet decided"
                
        grade_data = [i.string for i in html.find("tr",class_="table_w").find_all("td")]
        grade_data=grade_data[1:-1]
                
        credits_to_graduate = [major_state] + grade_data
        self.studentinfo_results.item_strings = credits_to_graduate
        self.studentinfo_results.adapter.data.clear()
        self.studentinfo_results.adapter.data.extend(credits_to_graduate)
        self.studentinfo_results._trigger_reset_populate()

class HufsGradeApp(App):
    pass

if __name__ == '__main__':
    HufsGradeApp().run()

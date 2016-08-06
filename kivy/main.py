from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button

import requests
from bs4 import BeautifulSoup
import re


head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
login_url = "https://webs.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp"
main_page = "http://webs.hufs.ac.kr:8989/src08/jsp/main.jsp?"
studentinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/stuinfo_10/STUINFO1000C_myinfo.jsp"

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
     
    def studentinfo(self):
        self.studentinfo=self.current_session.get(studentinfo_url,headers=head)
        html = BeautifulSoup(self.studentinfo.text, "html.parser")
        
        student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
        student_major = student_college.next_element.next_element.next_element.next_element.string
        student_id= html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
        student_name = html.find(string=re.compile('성명')).parent.parent.next_sibling.next_element.next_element.next_element.next_sibling.next_sibling.string
        student_name = student_name.replace("\r\n\t\t\t\t","")
        
        studentinfo = [student_college, student_major, student_id, student_name]
        self.studentinfo_results.item_strings = studentinfo

# 소속(ResultSet): html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.stripped_strings
# 학번: html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
# 성명: html.find(string=re.compile('성명')).parent.next_sibling.next_sibling.next_sibling.next_sibling.string

class HufsGradeApp(App):
    pass

if __name__ == '__main__':
    HufsGradeApp().run()

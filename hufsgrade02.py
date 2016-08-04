import requests
from bs4 import BeautifulSoup
import getpass

from kivy.app import App
from kivy.uix.widget import Widget
import re

#headers=head의 역할
#params vs data=params

head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
login_url = "https://webs.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp"
main_page = "http://webs.hufs.ac.kr:8989/src08/jsp/main.jsp?"
studentinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/stuinfo_10/STUINFO1000C_myinfo.jsp"


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

        for major in html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.stripped_strings:
            major = major.replace("(","")
            major = major.replace(")","")
            print(major)

        print(html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string)
        print(html.find(string=re.compile('성명')).parent.next_sibling.next_sibling.next_sibling.next_sibling.string)

# 소속(ResultSet): html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.stripped_strings
# 학번: html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
# 성명: html.find(string=re.compile('성명')).parent.next_sibling.next_sibling.next_sibling.next_sibling.string


if __name__ == '__main__':
    p = parse_score()
    p.login()
    p.studentinfo()
    
    

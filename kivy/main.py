from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest

import requests
from bs4 import BeautifulSoup

head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
login_url = "https://webs.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp"
main_page = "http://webs.hufs.ac.kr:8989/src08/jsp/main.jsp?"
studentinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/stuinfo_10/STUINFO1000C_myinfo.jsp"

class LoginForm(BoxLayout):    
    id_input = ObjectProperty()
    pwd_input = ObjectProperty()
    
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
        
        for dummy in html.find_all('td', {'class':'table_wl'}):
            for dummy2 in dummy.stripped_strings:
                print(dummy2)
                self.studentinfo_results.item_strings = dummy2

        

class HufsGradeApp(App):
    pass

if __name__ == '__main__':
    HufsGradeApp().run()

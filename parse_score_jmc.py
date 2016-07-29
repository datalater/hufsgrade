import requests
from bs4 import BeautifulSoup
import getpass

head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
login_url="https://webs.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp"
my_page="http://builder.hufs.ac.kr/user/indexFrame.action?framePath=div2_row_1.jsp&siteId=hufs&leftPage=&rightPage=08.html"
score_url="http://http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_List.jsp?tab_lang=K"
preview_score_url="http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_Top.jsp?tab_lang=K"


class parse_score():

    def __init__(self): #인스턴스를 만들 때 항상 실행된다. 인스턴스: 클래스를 상속받은 객체(클래스를 이용할 수 있는 객체) e.g. jmc = parse_score()
        self.user_id=input("id를 입력하세요: ")
        self.pwd=getpass.getpass("비밀번호를 입력하세요: ")
        print(self.user_id+"   "+self.pwd)
        
    def login(self):
        self.current_session=requests.session()
        
        params={"user_id":self.user_id,"password":self.pwd,"SSL_Login":1,"gubun":"o","reurl":""}
        self.current_session.post(login_url,data=params,headers=head)
        self.current_session.get(my_page,headers=head)
        

    def preview(self):
        self.preview_score=self.current_session.get(preview_score_url,headers=head)
        print(self.preview_score.text)

    



if __name__=="__main__":
    p=parse_score()
    p.login()
    p.preview()

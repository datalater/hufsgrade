import requests
from bs4 import BeautifulSoup
import getpass

import re
import time

#headers=head의 역할
#params vs data=params

head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
login_url = "https://webs.hufs.ac.kr/src08/jsp/login/LOGIN1011M.jsp"
main_page = "http://webs.hufs.ac.kr:8989/src08/jsp/main.jsp?"
studentinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/stuinfo_10/STUINFO1000C_myinfo.jsp"
gradeinfo_url = "http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_Top.jsp?tab_lang=K"
credits_list_url = "http://webs.hufs.ac.kr:8989/src08/jsp/grade/GRADE1030L_List.jsp?tab_lang=K"

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
        self.creditsinfo=self.current_session.get(credits_list_url,headers=head)
        html = BeautifulSoup(self.creditsinfo.text, "html.parser")

        grade_dic = {'A+':4.5, 'A0':4.0, 'B+':3.5, 'B0':3.0, 'C+':2.5, 'C0':2.0, 'D+':1.5, 'D0':1.0, 'F':0}

        first_major_credits = []
        first_major_times = []
        first_major_times_float = []
        first_major_multiply = []
        
        for td in html.find_all("tr",class_="table_w"):
            for td_first_major in td.find_all(string=re.compile('1전공')):
                for td_credits in td_first_major.parent.next_sibling.next_sibling:
                    first_major_credits.append(float(td_credits))
                for td_times in td_first_major.parent.next_sibling.next_sibling.next_sibling.next_sibling:
                    first_major_times.append(td_times)
        print(first_major_credits)
        print(first_major_times)
        print("------------------------------------------------------")
        for element in first_major_times:
            first_major_times_float.append(grade_dic[element])
        print(first_major_times_float)

        first_major_credits= list(map(float, first_major_credits))
        for i in range(len(first_major_credits)):
            first_major_multiply.append(first_major_credits[i] * first_major_times_float[i])
        print(first_major_multiply)
        print(round(sum(first_major_multiply)/sum(first_major_credits),2))
        

        
        
        self.studentinfo=self.current_session.get(studentinfo_url,headers=head)
        html = BeautifulSoup(self.studentinfo.text, "html.parser")

        #print(html.text)

        student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
        student_major = student_college.next_element.next_element.next_element.next_element.string
        student_id= html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
        student_name = html.find(string=re.compile('성명')).parent.parent.next_sibling.next_element.next_element.next_element.next_sibling.next_sibling.string
        student_name = student_name.replace("\r\n\t\t\t\t","")
        test = html.find(string=re.compile('성명')).parent.next_sibling.next_sibling.next_sibling.next_sibling.string
        print("---------------------------------------------------------")
        print(student_college)
        print(student_major)
        print(student_id)
        print(student_name)
        print(test)
        print("---------------------------------------------------------")


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
        #credits_completed = list(map(int, credits_completed))
        #grade_per_average = list(map(float, grade_per_average))
        credits_to_graduate = [major_state] + credits_completed + grade_per_average
        print(credits_to_graduate)        

        #2015~학번(사범대 제외)
        #dual_major_required = [54, 42, 0, 6, 26, 0, 0, 6, 134]
        #minor_required = [70, 0, 0, 6, 26, 21, 0, 11, 134]
      
        #2007~2014학번(사범대 제외)
        dual_major_required = ['Dual major required', 54, 54, 0, 4, 22, 0, 0, 0, 134, 4.5]
        minor_required = ['Minor required', 75, 0, 0, 4, 22, 21, 0, 12, 134, 4.5]
        dual_major_required = list(map(str, dual_major_required))
        minor_required = list(map(str, minor_required))

        versus_list = ['versus: ', 'first major: ', 'dual major: ', 'double major: ', 'practical foreign language: ', 'liberal arts: ', 'minor: ', 'teaching: ', 'free: ', 'total: ', 'GPA: ']

        print(len(versus_list))
        print(len(credits_to_graduate))
        print(len(dual_major_required))
         
        for i in range(len(versus_list)):
            versus_list[i] = versus_list[i]+credits_to_graduate[i] + " / " + dual_major_required[i]
        print(versus_list)
        


# 소속대학: student_college = html.find(string=re.compile('소속')).parent.next_sibling.next_sibling.next_element.next_element.string
# 소속학과: student_major = student_college.next_element.next_element.next_element.next_element.string
# 학번: student_id = html.find(string=re.compile('학번')).parent.next_sibling.next_sibling.string
# 성명: student_name = html.find(string=re.compile('성명')).parent.next_sibling.next_sibling.next_sibling.next_sibling.string
# 성명: student_name = student_name.replace("\r\n\t\t\t\t","")


        


if __name__ == '__main__':
    p = parse_score()
    p.login()
    p.studentinfo()
    
    

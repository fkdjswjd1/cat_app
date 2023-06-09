import streamlit as st
from streamlit_option_menu import option_menu
from Diagnosing_eye import Diagnosing_eye_page
from member.service import MemberService
from Signup import signup_page
from Login_Logout import login_page
from logout import logout_page
from Mypage import Mypage_page
import AI_Chatbot
from Write_life import Daylist_page
from Diagnosing_album import Diagnosing_album_page
import About
from guide_Hospital import Hospital_page
from pet.petsv import PetService

class Home:
    def __init__(self):
        self.signup=signup_page()
        self.login=login_page()
        self.logout=logout_page()
        self.service=MemberService()
        self.Mypage = Mypage_page()
        self.Daylist=Daylist_page()
        self.album=Diagnosing_album_page()
        self.eye=Diagnosing_eye_page()
        self.hospital=Hospital_page()
        self.petsv=PetService()
    def run(self):
        st.set_page_config(
            page_title='냥이의 하루, 안냥 ',
            page_icon=':cat:',
            layout='wide',  # wide,centered
            menu_items={
                'Get Help': 'https://lc.multicampus.com/k-digital/#/login',  # 페이지로 이동하기
                'About': '### 대박징조의 *반려묘의 안구질환 진단 및 하루 기록 서비스* 입니다.'
            },
            initial_sidebar_state='expanded'
        )
        # 사이드바
        if self.service.login_user(print=False) == '':
            login_logout = 'login'
        else:
            login_logout = 'logout'
        menu = ["Home", "Signup",  "Mypage",login_logout]
        with st.sidebar:
            choose = option_menu(MemberService.loginId, menu,
                                 icons=['house', 'bi-clipboard-check', 'gear','person lines fill' ],
                                  default_index=0,
                                 # styles={
                                 #     "container": {"padding": "5!important", "background-color": "#fafafa"},
                                 #     "icon": {"color": "orange", "font-size": "25px"},
                                 #     "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                 #                  "--hover-color": "#eee"},
                                 #     "nav-link-selected": {"background-color": "#02ab21"},
                                 # }
                                 )

        # 화면
        def bar():
            col, col1, col2,col3 = st.columns([2, 3, 1,1])
            with col1:
                st.title('냥이의 하루, 안냥:cat:')
            with col2:
                # if self.service.login_user(print=False) == '':
                #     login_logout = 'login'
                # else:
                #     login_logout = 'logout'
                st.write('#')
                self.service.login_user()
            with col3:
                self.petsv.printMyCat(print1=False)

            st.write('#')

            nav = ["About", "Diagnosing eye", "Medical charts", "AI Chatbot", "Write life", "Hospital"]
            select = option_menu(None, nav,
                                 icons=['house', 'camera fill', 'bi-folder2-open', 'bi-chat-dots', 'book', 'hospital'],
                                 default_index=0,
                                 styles={
                                     "container": {"padding": "5!important", "background-color": "#fafafa"},
                                     "icon": {"color": "orange", "font-size": "25px"},
                                     "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                  "--hover-color": "#eee"},
                                     "nav-link-selected": {"background-color": "#02ab21"}
                                 }, orientation="horizontal"
                                 )


            if select == nav[0]:
                About.About_page()
            if select == nav[1]:
                self.eye.diagnosing_eye_page()
            if select == nav[2]:
                self.album.run()
            if select == nav[3]:
                AI_Chatbot.AI_Chatbot_page()
            if select == nav[4]:
                self.Daylist.run()
            if select == nav[5]:
                self.hospital.run()

        # self.service.login_user()
        # st.markdown("---")


        def main():
            if choose == menu[0]:
                # About.About_page()
                bar()
            if choose == menu[1]:
                self.signup.run()
            if choose == menu[3]:
                self.login.run()
            if choose == menu[2]:
                self.Mypage.run()

        main()






if __name__== '__main__':
    m=Home()
    m.run()
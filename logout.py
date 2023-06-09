import streamlit as st
from member.service import MemberService
class logout_page:
    def __init__(self):
        self.service=MemberService()

    def run(self):
        logout_btn = st.sidebar.button('로그아웃')
        if logout_btn:

            self.service.logout()


if __name__ == '__main__':
    m = logout_page()
    m.run()
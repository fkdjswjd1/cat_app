import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import MarkerCluster
import sqlite3
from member.service import MemberService
from pet.petsv import PetService
from Hospital.hospital_db import HosptialDao


class Hospital_page:
    def __init__(self):
        self.hospitaldb=HosptialDao()
        self.petsv=PetService()
    def run(self):
        st.subheader('동물병원 정보')
        self.petsv.printMyCat(print2=False)

        if MemberService.loginId == '':
            return

        else:

            st.write(' ')
            row=self.hospitaldb.select_si()
            option = st.selectbox("###### 👇 지역 선택", row)
            if option in option:
                row2=self.hospitaldb.select_gu(option)
                option2 = st.selectbox("###### 👇 세부지역 선택", row2)
                if option2 in option2:
                    st.write(' ')
                    st.caption('❕아이콘을 클릭하면 전화번호와 영업시간을 안내해드립니다.')
                    lat_avg = self.hospitaldb.find_avg(col_name='Latitude',si=option,gu=option2)
                    lon_avg = self.hospitaldb.find_avg(col_name='Longitude',si=option,gu=option2)

                    m = folium.Map(width=400,height=500,location=[lat_avg, lon_avg],
                                   zoom_start=13, control_scale=True)

                    row_data=self.hospitaldb.allinfo(si=option,gu=option2)
                    col=['동물병원명','주소','운영시간','전화번호','Latitude','Longitude','Hospital_Si','Hospital_Gu']
                    df=pd.DataFrame(data=row_data,columns=col)
                    printdf=df.iloc[:,:4]
                    col1,col2=st.columns([2,3])
                    with col1:
                        for i in row_data:
                            html = f'''<p>{i[0]}<p/>
                                       <p>전화번호: {i[3]}<p/>
                                       <p>영업시간: {i[2]}<p/>
                                    '''

                            iframe = folium.IFrame(html)
                            popup = folium.Popup(iframe, min_width=300, max_width=300)
                            folium.Marker(location=[i[4], i[5]],
                                          popup=popup,
                                          tooltip=i[0]).add_to(m)

                        st_folium(m)
                    with col2:
                        st.table(printdf)



if __name__ == '__main__':
    m = Hospital_page()
    m.run()
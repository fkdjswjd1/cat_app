import io
import streamlit as st
from member.service import MemberService
from pet.petsv import PetService
from MedicalCharts.chart_db import ChartDao
from PIL import Image

class Diagnosing_album_page:
    def __init__(self):
        self.petsv=PetService()
        self.chartdb=ChartDao()

    def run(self):

        self.petsv.printMyCat(print2=False)
        mycat=PetService.loginCatName
        if MemberService.loginId=="":
            return
        elif mycat=="":
            st.error('마이페이지에서 반려묘를 등록해주세요')
        else:
            st.subheader(f'{mycat}의 진단기록📋')
            cat_info = self.petsv.printCatInfo(MemberService.loginId, mycat)

            Dates=self.chartdb.findDate(cat_info[3])
            for Date in Dates:
                with st.expander(label=Date):
                    images=self.chartdb.select1(cat_info[3],Date)
                    for name, img,Blepharitis, Blepharitis_percent, Deep_keratitis, Deep_keratitis_percent, Conjunctivitis,Conjunctivitis_percent, Conael_sequestrum, Conael_sequestrum_percent, Corneal_ulcer, Corneal_ulcer_percent in images:
                        col1,col2=st.columns(2)
                        col1.image(Image.open(io.BytesIO(img)), caption=name, width=200)
                        col2.write('안검염: '+Blepharitis+'('+Blepharitis_percent+'%)')
                        col2.write('비궤양성각막염: '+ Deep_keratitis+ '('+ Deep_keratitis_percent+ '%)')
                        col2.write('결막염: '+ Conjunctivitis+ '('+ Conjunctivitis_percent+ '%)')
                        col2.write('각막부골편: '+ Conael_sequestrum+ '('+ Conael_sequestrum_percent+ '%)')
                        col2.write('각막궤양: '+ Corneal_ulcer+ '('+ Corneal_ulcer_percent+ '%)')
                        st.markdown("---")


if __name__=='__main__':
    m=Diagnosing_album_page()
    m.run()
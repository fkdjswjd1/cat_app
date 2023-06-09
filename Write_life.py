import decimal
import math

import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import tensorflow as tf
from member.service import MemberService
from pet.petsv import PetService
import datetime
from MedicalCharts.chart_db import ChartDao
import io
import plotly.graph_objects as go
import plotly.express as px


class Diagnosing_eye_page:

    def __init__(self):
        self.service = MemberService()
        self.petsv = PetService()
        self.chartdb = ChartDao()

    def classification(self, img, weights_file):

        # Load your trained model
        model = tf.keras.models.load_model(weights_file)
        # Load and preprocess the new image
        image = img.resize((224, 224))  # Resize the image to match the input size of your model
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = tf.expand_dims(image, axis=0)  # Add an extra dimension to represent the batch
        # Normalize the image
        image = image / 255.0  # Assuming your model was trained with pixel values between 0 and 255
        # Make predictions
        prediction = model.predict(image)[0][0]  # Get the prediction value
        # Define the class labels
        class_labels = ['유', '무']  # Replace with your actual class labels
        # Set a threshold for classification (e.g., 0.5)
        threshold = 0.5
        # Determine the predicted class label
        predicted_class_label = class_labels[int(prediction >= threshold)]  # 0.5 미만: 유, 0.5 이상:무
        print(predicted_class_label)
        prediction = 1 - prediction  # 0.5 미만: 무, 0.5 이상:유
        print(prediction)
        decimal_prediction = decimal.Decimal(prediction)
        prediction = (decimal_prediction * 10000).quantize(decimal.Decimal('0.00')) / 100
        print(prediction)
        # Print the predicted class label
        return predicted_class_label, prediction

    def diagnosing_eye_page(self):
        font_css = """
                    <style>
                    button[data-baseweb="tab"]   {
                      background: #EAEAEA55;
                    }
                    </style>
                    """

        st.write(font_css, unsafe_allow_html=True)

        self.petsv.printMyCat(print2=False, print1=False)
        mycat = PetService.loginCatName

        if mycat:
            tabname = f"{mycat}의 진단 기록📋"
        else:
            tabname = "진단 기록📋"

        listtabs = ["안구질환 진단:eye:", tabname]
        whitespace = 30

        tabs = st.tabs([s.center(whitespace, "\u2001") for s in listtabs])
        with tabs[0]:
            if MemberService.loginId == "":
                st.error('로그인 먼저 하세요', icon="🚨")
            elif mycat == "":
                st.error('마이페이지에서 반려묘를 등록해주세요')
            else:
                col1, col, col2 = st.columns([3, 0.5, 2])
                cat_info = self.petsv.printCatInfo(MemberService.loginId, mycat)
                now = datetime.datetime.now()
                year = int(now.strftime('%Y'))
                month = int(now.strftime('%m'))
                day = int(now.strftime('%d'))
                today = datetime.date(year, month, day)

                with col1:
                    st.markdown('''
                    고양이의 안구질환은 조기에 치료하지 않으면 큰 질병까지 이어질 수 있습니다.
                    그러니 이 서비스를 이용하여 주기적으로 진단받으세요. 

                    ###### [서비스 이용방법]
                    1. 고양이의 눈만 보이도록 사진을 찍습니다.
                    2. 사진을 업로드하면 진단이 진행됩니다.
                    3. 결과와 질환에 대한 통계를 확인합니다.''')

                    st.caption('AI챗봇에 질환에 대해 물어보면 더 많은 정보를 얻을 수 있습니다.')
                    with st.expander('📸 예시 사진보기'):
                        imgcol1, imgcol2, imgcol3 = st.columns(3)
                        imgcol1.image('image/crop_C7_3e00fdab-60a5-11ec-8402-0a7404972c70.jpg',
                                      caption='손으로 눈을 벌리고 사진을 찍습니다.', width=150)
                        imgcol2.image('image/crop_C1_3e075e5a-60a5-11ec-8402-0a7404972c70.jpg',
                                      caption='눈 부위를 밝게 찍습니다.', width=150)
                        imgcol3.image('image/crop_C42_3e00a570-60a5-11ec-8402-0a7404972c70.jpg',
                                      caption='눈동자에 비치는 것이 없도록 찍습니다.', width=150)
                    with st.expander('📌 읽어보세요!!'):
                        st.markdown('- 사진의 각도에 따라서 결과가 다르게 나올 수 있습니다.')
                        st.markdown('- 여러번 시도 해보세요')
                        st.markdown('- 해당 서비스는 참고용으로만 사용해주세요')

                uploaded_image = st.file_uploader("이미지를 업로드하세요.", type=["jpg"], label_visibility='collapsed')

                with col2:
                    st.markdown('###### 업로그 사진 보기')
                    if uploaded_image is not None:
                        image = Image.open(uploaded_image)
                        st.image(image, caption='Uploaded Image.', width=300)
                if uploaded_image is not None:
                    st.write('')
                    class_list = ['안검염', '비궤양성각막염', '결막염', '각막부골편', '각막궤양']
                    model_list = ['model/b.h5', 'model/d.h5', 'model/conjun.h5', 'model/conael_s.h5',
                                  'model/corneal_u.h5']
                    predicted_class_list = []  # 유,무 리스트
                    prediction_list = []
                    with st.spinner('처리중입니다...(20초 이내)'):
                        for i, model in enumerate(model_list):
                            predicted_class_label, prediction = self.classification(image, model)
                            predicted_class_list.append(predicted_class_label)
                            prediction_list.append(str(prediction))

                    yes_class = []
                    yes_pred = []
                    for i, pcl in enumerate(predicted_class_list):
                        if pcl == '유':
                            yes_class.append(class_list[i])
                            yes_pred.append(prediction_list[i])

                    total = ''
                    for i in range(len(yes_class)):
                        total = total + yes_class[i] + '(' + yes_pred[i] + '%)' + ', '
                    newtotal = total.rstrip(', ')

                    if '유' in predicted_class_list:
                        st.success(f'해당 사진은 **{newtotal}** 이 예상됩니다. \n\n 가까운 병원에 가셔서 정확한 진단을 받아보세요', icon='😿')
                    else:
                        st.success('해당 사진에는 보이는 질환이 없습니다. 건강합니다.', icon='😸')

                    # db 저장
                    image_name = now
                    self.chartdb.upload_image1(cat_info[3], today,
                                               image_name, uploaded_image,
                                               predicted_class_list[0], prediction_list[0],
                                               predicted_class_list[1], prediction_list[1],
                                               predicted_class_list[2], prediction_list[2],
                                               predicted_class_list[3], prediction_list[3],
                                               predicted_class_list[4], prediction_list[4]
                                               )
        with tabs[1]:
            if MemberService.loginId == "":
                st.error('로그인 먼저 하세요', icon="🚨")
            elif mycat == "":
                st.error('마이페이지에서 반려묘를 등록해주세요')
            else:
                cat_info = self.petsv.printCatInfo(MemberService.loginId, mycat)

                Dates = self.chartdb.findDate(cat_info[3])
                if Dates:
                    for Date in Dates:
                        with st.expander(label=f' {Date}'):
                            images = self.chartdb.select1(cat_info[3], Date)
                            for name, img, Blepharitis, Blepharitis_percent, Deep_keratitis, Deep_keratitis_percent, Conjunctivitis, Conjunctivitis_percent, Conael_sequestrum, Conael_sequestrum_percent, Corneal_ulcer, Corneal_ulcer_percent in images:
                                col1, col2, col3 = st.columns([1, 1, 2])
                                col1.write('##### 🖼️업로드한 사진')
                                col1.image(Image.open(io.BytesIO(img)), caption=name, width=200)
                                col2.write('##### 📃의심되는 질병')
                                if Blepharitis == '유':
                                    col2.write('안검염')
                                if Deep_keratitis == '유':
                                    col2.write('비궤양성각막염')
                                if Conjunctivitis == '유':
                                    col2.write('결막염')
                                if Conael_sequestrum == '유':
                                    col2.write('각막부골편')
                                if Corneal_ulcer == '유':
                                    col2.write('각막궤양')
                                if Blepharitis == '무' and Deep_keratitis == '무' and Conjunctivitis == '무' and Conael_sequestrum == '무' and Corneal_ulcer == '무':
                                    col2.write('의심되는 질병이 없습니다.')
                                with col3:
                                    data = {'col': ['안검염', '비궤양성각막염', '결막염', '각막부골편', '각막궤양'],
                                            'value': [float(Blepharitis_percent),
                                                      float(Deep_keratitis_percent),
                                                      float(Conjunctivitis_percent),
                                                      float(Conael_sequestrum_percent),
                                                      float(Corneal_ulcer_percent)]}
                                    df = pd.DataFrame(data=data)
                                    # st.dataframe(df)
                                    fig1 = px.bar(x=df['col'], y=df['value'], text=df['value'],
                                                  color_discrete_sequence=['#FFC19E'])
                                    fig1.update_traces(textposition='auto')

                                    fig1.add_trace(px.line(x=df['col'], y=[50] * len(df),
                                                           color_discrete_sequence=['#FF5E00']).data[0])

                                    fig1.update_layout(
                                        xaxis=dict(title=''),
                                        yaxis=dict(title='질병일 확률', range=[0, 100]),
                                        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                                        width=400, height=300
                                    )
                                    st.plotly_chart(fig1)
                                    # st.dataframe(df)
                                st.markdown("---")
                else:
                    st.error('안구질환 진단한 기록이 없습니다!')


if __name__ == '__main__':
    m = Diagnosing_eye_page()
    m.diagnosing_eye_page()


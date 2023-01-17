$ conda install -c plotly plotly=5.11.0
import streamlit as st
import plotly as px
import pandas as pd
import os
import datetime
import numpy as np

    
with st.sidebar:
    d = st.date_input(
    "기준일 선택",
    datetime.date(2022, 9, 30))
    st.write('기준일:', d)
    c = st.selectbox('본부를 선택하세요.', ("CM1", "CM2", "ICE1","ICE2","ICE3","IGH","IM1","IM2","IM3","IM4"))
    
    
df = pd.read_csv('lob_corps.csv', encoding = 'euc-kr')

st.subheader('Engagement별 리스크 식별 현황')
st.write(c,'본부의', d.strftime("%Y년%m월%d일"),'기준 Engagement별 리스크 식별 현황입니다.')
st.write('원의 크기는 식별된 위험지표의 개수에 비례하여 증가합니다.')
fig = px.scatter(
df[(df['기준일']== d.strftime("%Y-%m-%d"))&(df['LoB']== c)],
x="자산총계",
y="매출액",
size="위험지표",
color="회사명",
hover_name="회사명",
log_x=True,
size_max=60,
)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)

risk_idx = pd.read_csv('risk_index.csv', encoding = 'euc-kr')
risk_idx_date = risk_idx[risk_idx['기준일'] ==  d.strftime("%Y-%m-%d")]
risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']== c]

columns_rename = {'1 표본심사':'표본심사', '2 개별감사업무 선정': '개별감사업무', '3 관리종목': '관리종목', '4 직권지정':'직권지정','5 기타':'기타'}

with st.expander("Plot chart 세부내용"):
    st.write('Engagement별 위험지표 식별 현황은 아래와 같습니다.')
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))
    
st.write('')
st.write('')
st.write('')

risk_idx_corps = risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename).reset_index()

st.subheader('감리 대상 업무 선정 가능성')
st.write('위험지표별로 감리 대상 업무로 선정될 가능성이 높은 Enagement는 다음과 같습니다.')
tab1, tab2, tab3 , tab4, tab5 = st.tabs(["표본심사", "개별감사업무", "관리종목","직권지정","기타"])

with tab1:
    st.write(risk_idx_corps['회사명'][risk_idx_corps['표본심사'] > 0])

with tab2:
    st.write(risk_idx_corps['회사명'][risk_idx_corps['개별감사업무'] > 0])
    
with tab3:
    st.write(risk_idx_corps['회사명'][risk_idx_corps['관리종목'] > 0])

with tab4:
    st.write(risk_idx_corps['회사명'][risk_idx_corps['직권지정'] > 0])
    
with tab5:
    st.write(risk_idx_corps['회사명'][risk_idx_corps['기타'] > 0])
    

st.write('')
st.write('')
st.write('')
st.write('Engagement별로 다음의 위험지표들이 식별되어 감리 대상 업무로 선정될 가능성이 높은 것으로 판단하였습니다.')

eng = st.selectbox('Engagement를 선택하세요.', tuple(set(risk_idx_date_lob['회사명'])))
risk_idx_total = risk_idx_date[(risk_idx_date['LoB']==c)&(risk_idx_date['값'] > 0)&(risk_idx_date['회사명'] == eng)].groupby(['회사명','지표구분','특성'])['값'].sum()
st.write(risk_idx_total)

st.write('')
st.write('')
st.write('')

st.subheader('전체 Table')
st.write('Engagement별 위험지표 식별 현황입니다.')
def convert_df(df):
    return df.to_csv().encode('euc-kr')

risk_idx_total = risk_idx_date[risk_idx_date['LoB']==c].groupby(['회사명','특성'])['값'].sum().unstack()
csv = convert_df(risk_idx_total)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='위험지표식별현황.csv',
    mime='text/csv',
)
st.write(risk_idx_total)

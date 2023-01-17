import streamlit as st
import pandas as pd
import os
import datetime
import numpy as np

risk_idx = pd.read_csv('risk_index.csv', encoding = 'euc-kr')

date_list =['2017-12-31', '2018-12-31', '2019-12-31', '2020-12-31','2021-12-31', '2022-09-30']

date_dic = { date_list[5]:date_list[4], date_list[4]:date_list[3], date_list[3]:date_list[2], date_list[2]:date_list[1],date_list[1]:date_list[0] }

with st.sidebar:
    d = st.date_input(
    "기준일 선택",
    datetime.date(2022, 9, 30))
    st.write('기준일:', d)

date_sel = d.strftime("%Y-%m-%d")
st.header('위험지표 식별현황')

date_compare = date_dic[date_sel]

rsk_idx_total = pd.pivot_table(risk_idx[risk_idx['기준일'].isin([date_sel, date_compare])], values = ['값'], index = ['지표구분'], columns = ['기준일'], aggfunc = np.sum)

pyobon = rsk_idx_total.iloc[0,1]
gyebyul = rsk_idx_total.iloc[1,1]
kwanri = rsk_idx_total.iloc[2,1]
jikkwon = rsk_idx_total.iloc[3,1]
etc = rsk_idx_total.iloc[4,1]
idx_total = pyobon+gyebyul+kwanri+jikkwon+etc

pyobon_delta = rsk_idx_total.iloc[0,1]-rsk_idx_total.iloc[0,0]
gyebyul_delta =  rsk_idx_total.iloc[1,1]-rsk_idx_total.iloc[1,0]
kwanri_delta = rsk_idx_total.iloc[2,1]-rsk_idx_total.iloc[2,0]
jikkwon_delta = rsk_idx_total.iloc[3,1]-rsk_idx_total.iloc[3,0]
etc_delta = rsk_idx_total.iloc[4,1]-rsk_idx_total.iloc[4,0]
delta_total = pyobon_delta+gyebyul_delta+kwanri_delta+jikkwon_delta+etc_delta

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("표본심사", pyobon.astype('str') ,pyobon_delta.astype('str'))
col2.metric("개별감사업무", gyebyul.astype('str') ,gyebyul_delta.astype('str'))
col3.metric("관리종목",kwanri.astype('str') ,kwanri_delta.astype('str'))
col4.metric("직권지정", jikkwon.astype('str') ,jikkwon_delta.astype('str'))
col5.metric("기타", etc.astype('str') ,etc_delta.astype('str'))
col6.metric("합계", idx_total.astype('str'), delta_total.astype('str'))

st.write('')
st.write('')
st.write('')


risk_idx_date = risk_idx[risk_idx['기준일'] == date_sel]
risk_idx_by_lob = risk_idx_date.groupby(['LoB','지표구분'])['값'].sum().unstack()
columns_rename = {'1 표본심사':'표본심사', '2 개별감사업무 선정': '개별감사업무', '3 관리종목': '관리종목', '4 직권지정':'직권지정','5 기타':'기타'}
risk_idx_by_lob = risk_idx_by_lob.rename(columns =columns_rename)

#col_1, col_2 = st.columns(2, gap = "large")

#with col_1:
risk_indx_date_grouped = risk_idx_date.groupby(['LoB'])['값'].sum()
chart_data = pd.DataFrame(
risk_indx_date_grouped,
index = ["CM1", "CM2", "ICE1","ICE2","ICE3","IGH","IM1","IM2","IM3","IM4"]
)
st.subheader('본부별 위험지표 식별 현황')
st.bar_chart(chart_data)
st.write('')
with st.expander("Bar chart 세부내용"):
    st.write('본부별 위험지표 식별 현황은 아래와 같습니다.')
    st.write(risk_idx_by_lob)

#with col_2: 
st.write('')
st.write('')
st.write('')

st.subheader('본부 Engagement별 위험지표 식별 현황')
st.write(d.strftime("%Y년%m월%d일"),' 기준 본부 Engagement의 위험지표 식별 현황은 아래와 같습니다.')

tab1, tab2, tab3 , tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["CM1", "CM2", "ICE1","ICE2","ICE3","IGH","IM1","IM2","IM3","IM4"])

with tab1:
    st.caption('Engagement별 위험식별 현황')
    risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']=='CM1']
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))

with tab2:
    st.caption('Engagement별 위험식별 현황')
    risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']=='CM2']
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))

with tab3:
    st.caption('Engagement별 위험식별 현황')
    risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']=='ICE1']
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))
    
with tab4:
    st.caption('Engagement별 위험식별 현황')
    risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']=='ICE2']
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))
    
with tab5:
    st.caption('Engagement별 위험식별 현황')
    risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']=='ICE3']
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))
    
with tab6:
    st.caption('Engagement별 위험식별 현황')
    risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']=='IGH']
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))
    
with tab7:
    st.caption('Engagement별 위험식별 현황')
    risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']=='IM1']
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))
    
with tab8:
    st.caption('Engagement별 위험식별 현황')
    risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']=='IM2']
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))

with tab9:
    st.caption('Engagement별 위험식별 현황')
    risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']=='IM3']
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))
    
with tab10:
    st.caption('Engagement별 위험식별 현황')
    risk_idx_date_lob = risk_idx_date[risk_idx_date['LoB']=='IM4']
    st.write(risk_idx_date_lob.groupby(['회사명','지표구분'])['값'].sum().unstack().rename(columns=columns_rename))

st.write('')
st.write('')
st.write('')

st.subheader('전체 Table')
st.write('Engagement별 위험지표 식별 현황입니다.')
def convert_df(df):
    return df.to_csv().encode('euc-kr')

risk_idx_total = risk_idx_date.groupby(['LoB','회사명','특성'])['값'].sum().unstack()
csv = convert_df(risk_idx_total)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='위험지표식별현황.csv',
    mime='text/csv',
)
st.write(risk_idx_total)
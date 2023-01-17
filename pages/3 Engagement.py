import streamlit as st
import plotly.express as px
import pandas as pd
import os
import datetime
import numpy as np

lob_corps = pd.read_csv('lob_corps.csv', encoding = 'euc-kr')


with st.sidebar:
    d = st.date_input(
    "기준일을 선택하세요.",
    datetime.date(2022, 9, 30))
    c = st.selectbox('본부를 선택하세요.', ("CM1", "CM2", "ICE1","ICE2","ICE3","IGH","IM1","IM2","IM3","IM4"))
    corp_list = tuple(set(lob_corps['회사명'][lob_corps['LoB']== c]))
    eng = st.selectbox('회사명을 입력하세요.', corp_list)
    
    
st.subheader('위험지표의 식별')
st.write('')
st.write('')
st.write('')

risk_idx = pd.read_csv('risk_index.csv', encoding = 'euc-kr')
risk_idx_selected = risk_idx[(risk_idx['회사명']== eng)&(risk_idx['기준일']==d.strftime("%Y-%m-%d"))].groupby('지표구분')['값'].sum().reset_index()

pyobon = risk_idx_selected.iloc[0,1]
gyebyul = risk_idx_selected.iloc[1,1]
kwanri = risk_idx_selected.iloc[2,1]
jikkwon = risk_idx_selected.iloc[3,1]
etc = risk_idx_selected.iloc[4,1]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("표본심사", pyobon.astype('str'))
col2.metric("개별감사업무", gyebyul.astype('str'))
col3.metric("관리종목",kwanri.astype('str'))
col4.metric("직권지정", jikkwon.astype('str'))
col5.metric("기타", etc.astype('str'))


st.write('')
st.write('')
st.write('')


st.write(d.strftime("%Y년%m월%d일"), eng,'에서 식별된 위험지표의 세부내용은 아래와 같습니다.')
risk_idx = pd.read_csv('risk_index.csv', encoding = 'euc-kr')
risk_idx_date = risk_idx[risk_idx['기준일'] ==  d.strftime("%Y-%m-%d")]
#columns_rename = {'1 표본심사':'표본심사', '2 개별감사업무 선정': '개별감사업무', '3 관리종목': '관리종목', '4 직권지정':'직권지정','5 기타':'기타'}
#risk_idx_date= risk_idx_date.rename(columns = columns_rename)
#risk_idx_date_eng = risk_idx_date[risk_idx_date['회사명']== eng]
risk_idx_char = risk_idx_date[(risk_idx_date['회사명']==eng)&(risk_idx_date['값']>0)].groupby(['지표구분','특성'])['값'].sum()
st.write(risk_idx_char)

st.write('')
st.write('')
st.write('')

st.subheader('RMM의 식별')
st.write(eng, '는 다음의 RM 중에서 RMM의 식별을 고려할 필요가 있습니다.')

corp_industry = pd.read_excel('corp_industry.xlsx', sheet_name = 'corp_industry')
rmm = pd.read_excel('corp_industry.xlsx', sheet_name = 'rmm')

industry_selected = corp_industry['Industry'][corp_industry['회사명']== eng].iloc[0]
rmm_selected = rmm[rmm['Industry']==industry_selected]
st.write(rmm_selected[['ClientID2','Description']])

st.write('')
st.write('')
st.write('')

fs_sampled = pd.read_csv('fs_sampled_industry.csv', encoding = 'euc-kr')




st.subheader('요약재무제표')
st.write(eng,'의',d.strftime("%Y년%m월%d일"),'기준 재무현황은 다음과 같습니다.')
tab_1, tab_2 = st.tabs(['연결','별도'])
with tab_1 :
    tab1, tab2= st.tabs(['재무상태표', '손익계산서'])
    with tab1:
        st.write(fs_sampled[['항목명','당기','전기']][(fs_sampled['연결/별도']=='연결')&(fs_sampled['재무제표구분']=='BS')&(fs_sampled['회사명']==eng)&(fs_sampled['결산기준일']==d.strftime("%Y-%m-%d"))])
    with tab2:
        st.write(fs_sampled[['항목명','당기','전기']][(fs_sampled['연결/별도']=='연결')&(fs_sampled['재무제표구분']=='PL')&(fs_sampled['회사명']==eng)&(fs_sampled['결산기준일']==d.strftime("%Y-%m-%d"))])

with tab_2:
    tab3, tab4= st.tabs(['재무상태표', '손익계산서'])
    with tab3:
        st.write(fs_sampled[['항목명','당기','전기']][(fs_sampled['연결/별도']=='별도')&(fs_sampled['재무제표구분']=='BS')&(fs_sampled['회사명']==eng)&(fs_sampled['결산기준일']==d.strftime("%Y-%m-%d"))])
    with tab4:
        st.write(fs_sampled[['항목명','당기','전기']][(fs_sampled['연결/별도']=='별도')&(fs_sampled['재무제표구분']=='PL')&(fs_sampled['회사명']==eng)&(fs_sampled['결산기준일']==d.strftime("%Y-%m-%d"))])




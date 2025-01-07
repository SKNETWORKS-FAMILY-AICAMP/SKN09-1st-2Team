# !pip install xlrd
# !pip install openpyxl
# pip install webdriver_manager
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px


year_list = [str(i) for i in range(2020,2025)]

data_dic = {}
# 연도별 자동차 등록현황 호출
for year in year_list:
    data_1 = pd.read_excel('data/'+ year +'년_11월_자동차_등록자료_통계.xlsx', sheet_name='10.연료별_등록현황',skiprows=2)
    if year in year[0:4]:
        data_1[['연료별','시도별']] = data_1[['연료별','시도별']].fillna(method='ffill')
    data_2 = data_1[(data_1['시도별'] == '소계') & (data_1['Unnamed: 2'] == "계")]
    data_2 = data_2.drop(['시도별','Unnamed: 2'], axis=1)

    # exec(f'data_{year} = data_2')
    data_dic['data_' + year] = data_2

# 좌표데이터
coordinate = pd.DataFrame({
    '지역' : ['서울','부산','강원','충북','충남','전북','전남','경북','경남','제주','대구','인천','광주','대전','울산','세종','경기'],
    '위도' : [37.5642135, 35.1379222, 37.8304115, 36.636040, 36.659082, 35.820371, 34.816078, 36.576047, 
            35.237722, 33.383148, 35.5217, 37.2702, 35.150762, 36.35111, 35.52534995, 36.2850, 37.5864315 ],
    '경도' : [127.0016985, 129.05562775, 128.2260705, 127.491507, 126.673079, 127.109135, 126.463203, 128.505757, 
            128.692008, 126.526199, 128.3605, 126.4215, 126.814830, 127.385, 129.22244165, 127.1720, 127.0462765]
})

# 친환경 자동차 목록(화석연료 차량 구하는데 사용)
eco_fuel = ['전기','태양열','하이브리드(휘발유+전기)','하이브리드(경유+전기)',
            '하이브리드(LPG+전기)','하이브리드(CNG+전기)','하이브리드(LNG+전기)','수소','수소전기'] # 수소전기는 24년도만

# Chart1
col1, col2 = st.columns(2)
hybrid = ['하이브리드(휘발유+전기)','하이브리드(경유+전기)',
            '하이브리드(LPG+전기)','하이브리드(CNG+전기)','하이브리드(LNG+전기)']# 하이브리드만
eco_fri = ['하이브리드(휘발유+전기)','하이브리드(경유+전기)',
            '하이브리드(LPG+전기)','하이브리드(CNG+전기)','하이브리드(LNG+전기)','전기'] # 친환경(하이브리드 + 전기기)

data_tmp = data_dic['data_'+'2024'][['연료별','계']][0:-1]
chart_data3 = pd.DataFrame({
    "연료" : ['화석연료','하이브리드','전기'],
    '등록대수' : [int(data_tmp[~data_tmp['연료별'].isin(eco_fuel)].sum()['계']),
              int(data_tmp[data_tmp['연료별'].isin(hybrid)].sum()['계']),
              int(data_tmp[data_tmp['연료별'] == '전기'].sum()['계'])]
})
chart_data3_1 = pd.DataFrame({
    "연료" : ['화석연료','친환경'],
    '등록대수' : [int(data_tmp[~data_tmp['연료별'].isin(eco_fuel)].sum()['계']),
              int(data_tmp[data_tmp['연료별'].isin(eco_fri)].sum()['계'])]
})

fig = px.pie(data_frame = chart_data3, values='등록대수', names='연료')
fig.update_traces(pull=[0.2, 0.2, 0])

fig1 = px.pie(data_frame = chart_data3_1, values='등록대수', names='연료')
fig1.update_traces(pull=[0.2, 0])


# Chart2
chart_data1 = pd.DataFrame({
    'year': [],
    'fuel': [],
    'num' : []
})

for year in year_list:
    data_tmp = data_dic['data_'+year][0:-1]
    eco_num = data_tmp[data_tmp['연료별'].isin(eco_fuel)]['계'].sum()
    fossil_num = data_tmp[~data_tmp['연료별'].isin(eco_fuel)]['계'].sum()

    new_rows1 = pd.DataFrame({'year': [year], 'fuel': ['eco'], 'num': [eco_num]})
    new_rows2 = pd.DataFrame({'year': [year], 'fuel': ['fussil'], 'num': [fossil_num]})

    chart_data1 = pd.concat([chart_data1, new_rows1, new_rows2], ignore_index=True)




with col1:
    st.write('전기, 하이브리드 자동차 수요')
    st.plotly_chart(fig, use_container_width=True)

    st.write('친환경, 화석연료 자동차 등록현황 연도별 비교')
    st.bar_chart(chart_data1, x = 'year', y='num', color='fuel', stack = False)
with col2:
    st.write('친환경 자동차 수요')
    st.plotly_chart(fig1, use_container_width=True)

    st.write('친환경 자동차 등록현황 연도별 비교')
    chart_data1_1 = chart_data1[chart_data1['fuel'] == 'eco']
    st.bar_chart(chart_data1_1, x = 'year', y='num', stack = False)






# Chart3
chart_data2 = data_dic["data_2024"].iloc[:,0:-1]
chart_data2_1 = chart_data2[chart_data2['연료별'].isin(eco_fuel)].sum()

chart_data2_2 = pd.DataFrame({
    '지역' : chart_data2_1.index[1:],
    '등록현황' : chart_data2_1.values[1:] / 10
})
chart_data2_2 = pd.merge(chart_data2_2, coordinate)

st.write('2024년 지역별 친환경 자동차 등록현황')

st.map(chart_data2_2, latitude="위도", longitude="경도", size="등록현황")
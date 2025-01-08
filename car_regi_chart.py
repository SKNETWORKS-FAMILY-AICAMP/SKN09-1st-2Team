import pymysql
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px


# MySQL 연결 설정
connection = pymysql.connect(
    host="192.168.0.20",
    user="team2",
    password="team2",
    database="team2",
    port=3306
)


cursor = connection.cursor()

sql = """select * from car_reg_info"""
cursor.execute(sql)
data = cursor.fetchall()

sql = """select* from region_info"""
cursor.execute(sql)
coordinate = cursor.fetchall()
cursor.close()
connection.close()


# 연도별 자동차 등록현황 호출
data1 = pd.DataFrame(data)
data1 = pd.DataFrame(data)
data1.columns = ['id','year','fuel','region','count']
data1 = data1.drop('id',axis=1)
data1['year'] = data1['year'].apply(lambda x : x[0:4])

# 좌표데이터
coordinate = pd.DataFrame(coordinate)
coordinate.columns = ['id','지역','위도','경도']
coordinate = coordinate.drop('id',axis=1)

# 친환경 자동차 목록(화석연료 차량 구하는데 사용)
eco_fuel = ['전기','태양열','하이브리드(휘발유+전기)','하이브리드(경유+전기)',
            '하이브리드(LPG+전기)','하이브리드(CNG+전기)','하이브리드(LNG+전기)','수소','수소전기'] # 수소전기는 24년도만

# Chart1
col1, col2 = st.columns(2)
hybrid = ['하이브리드(휘발유+전기)','하이브리드(경유+전기)',
            '하이브리드(LPG+전기)','하이브리드(CNG+전기)','하이브리드(LNG+전기)']# 하이브리드만
eco_fri = ['하이브리드(휘발유+전기)','하이브리드(경유+전기)',
            '하이브리드(LPG+전기)','하이브리드(CNG+전기)','하이브리드(LNG+전기)','전기'] # 친환경(하이브리드 + 전기기)

data_tmp = data1[data1['year'] == '2024']
chart_data3 = pd.DataFrame({
    "연료" : ['화석연료','하이브리드','전기'],
    '등록대수' : [int(data_tmp[~data_tmp['fuel'].isin(eco_fuel)].sum()['count']),
              int(data_tmp[data_tmp['fuel'].isin(hybrid)].sum()['count']),
              int(data_tmp[data_tmp['fuel'] == '전기'].sum()['count'])]
})
chart_data3_1 = pd.DataFrame({
    "연료" : ['화석연료','친환경'],
    '등록대수' : [int(data_tmp[~data_tmp['fuel'].isin(eco_fuel)].sum()['count']),
              int(data_tmp[data_tmp['fuel'].isin(eco_fri)].sum()['count'])]
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
year_list = [str(i) for i in range(2020,2025)]
for year in year_list:
    data_tmp = data1[data1['year'] == year]
    eco_num = data_tmp[data_tmp['fuel'].isin(eco_fuel)]['count'].sum()
    fossil_num = data_tmp[~data_tmp['fuel'].isin(eco_fuel)]['count'].sum()

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
chart_data2 = data1[data1['year'] == '2024']
chart_data2_1 = chart_data2[chart_data2['fuel'].isin(eco_fuel)]
chart_data2_1 = chart_data2_1.groupby('region')['count'].sum()

chart_data2_2 = pd.DataFrame({
    '지역' : chart_data2_1.index[1:],
    '등록현황' : chart_data2_1.values[1:] / 10
})
chart_data2_2 = pd.merge(chart_data2_2, coordinate)

st.write('2024년 지역별 친환경 자동차 등록현황')

st.map(chart_data2_2, latitude="위도", longitude="경도", size="등록현황")
import pymysql
import pandas as pd
import streamlit as st
import plotly.express as px

def run():
    st.title("📊 등록 현황")

    # Markdown 문법으로 제목 및 서브 제목 꾸미기
    st.markdown("""
    <h3 style='color: #FF6347;'>지역별 및 연료별 등록 현황</h3>
    친환경 자동차의 최신 현황 데이터를 이용해 트렌드를 분석합니다.
    """, unsafe_allow_html=True)

    st.markdown("<h5 style='font-size: 16px;'>국내 지역별 / 연료별 자동차의 등록 결과를 확인할 수 있습니다.</h5>", unsafe_allow_html=True)

    # 텍스트 강조 및 정보 표시
    st.info("💡 **이 분석은 2024년 기준으로 지역별, 연료별 자동차 등록 현황을 시각화한 것입니다.**")

    # MySQL 연결 설정
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="carsystemdb"
    )

    cursor = connection.cursor()

    sql = """select * from car_reg_info"""
    cursor.execute(sql)
    data = cursor.fetchall()

    sql = """select * from region_info"""
    cursor.execute(sql)
    coordinate = cursor.fetchall()
    cursor.close()
    connection.close()

    data1 = pd.DataFrame(data)
    data1.columns = ['id', 'year', 'region', 'fuel', 'count']
    data1 = data1.drop('id', axis=1)
    data1['year'] = data1['year'].apply(lambda x: x[0:4])

    if data1[['year', 'fuel', 'region', 'count']].isnull().any().any():
        st.warning("Some data is missing in 'year', 'fuel', 'region', or 'count' columns.")

    data1['count'] = pd.to_numeric(data1['count'], errors='coerce')

    # 좌표데이터
    coordinate = pd.DataFrame(coordinate)
    coordinate.columns = ['id', '지역', '위도', '경도']
    coordinate = coordinate.drop('id', axis=1)

    # Check for missing coordinates
    if coordinate[['위도', '경도']].isnull().any().any():
        st.warning("Some coordinates are missing (위도, 경도).")

    coordinate['위도'] = pd.to_numeric(coordinate['위도'], errors='coerce')
    coordinate['경도'] = pd.to_numeric(coordinate['경도'], errors='coerce')

    # 친환경 자동차 목록(화석연료 차량 구하는데 사용)
    eco_fuel = ['전기', '태양열', '하이브리드(휘발유+전기)', '하이브리드(경유+전기)',
                '하이브리드(LPG+전기)', '하이브리드(CNG+전기)', '하이브리드(LNG+전기)', '수소', '수소전기']  # 수소전기는 24년도만

    # Chart1
    col1, col2 = st.columns(2)
    hybrid = ['하이브리드(휘발유+전기)', '하이브리드(경유+전기)',
              '하이브리드(LPG+전기)', '하이브리드(CNG+전기)', '하이브리드(LNG+전기)']  # 하이브리드만
    eco_fri = ['하이브리드(휘발유+전기)', '하이브리드(경유+전기)',
               '하이브리드(LPG+전기)', '하이브리드(CNG+전기)', '하이브리드(LNG+전기)', '전기']  # 친환경(하이브리드 + 전기기)

    data_tmp = data1[data1['year'] == '2024']
    print(data_tmp['fuel'].unique())
    chart_data3 = pd.DataFrame({
        "연료": ['화석연료', '하이브리드', '전기'],
        '등록대수': [int(data_tmp[~data_tmp['fuel'].isin(eco_fuel)].sum()['count']),
                     int(data_tmp[data_tmp['fuel'].isin(hybrid)].sum()['count']),
                     int(data_tmp[data_tmp['fuel'] == '전기'].sum()['count'])],
    })
    chart_data3_1 = pd.DataFrame({
        "연료": ['화석연료', '친환경'],
        '등록대수': [int(data_tmp[~data_tmp['fuel'].isin(eco_fuel)].sum()['count']),
                     int(data_tmp[data_tmp['fuel'].isin(eco_fri)].sum()['count'])],
    })
    fig = px.pie(data_frame=chart_data3, values='등록대수', names='연료')
    fig.update_traces(pull=[0.2, 0.2, 0])

    fig1 = px.pie(data_frame=chart_data3_1, values='등록대수', names='연료')
    fig1.update_traces(pull=[0.2, 0])

    # Chart2
    chart_data1 = pd.DataFrame({
        'year': [],
        'fuel': [],
        'num': []
    })
    year_list = [str(i) for i in range(2020, 2025)]
    for year in year_list:
        data_tmp = data1[data1['year'] == year]
        eco_num = data_tmp[data_tmp['fuel'].isin(eco_fuel)]['count'].sum()
        fossil_num = data_tmp[~data_tmp['fuel'].isin(eco_fuel)]['count'].sum()

        new_rows1 = pd.DataFrame({'year': [year], 'fuel': ['eco'], 'num': [eco_num]})
        new_rows2 = pd.DataFrame({'year': [year], 'fuel': ['fossil'], 'num': [fossil_num]})

        chart_data1 = pd.concat([chart_data1, new_rows1, new_rows2], ignore_index=True)

    with col1:
        st.write('전기, 하이브리드 자동차 수요')
        st.plotly_chart(fig, use_container_width=True)

        st.write('친환경, 화석연료 자동차 등록현황 연도별 비교')
        st.bar_chart(chart_data1, x='year', y='num', color='fuel', stack=False)
    with col2:
        st.write('친환경 자동차 수요')
        st.plotly_chart(fig1, use_container_width=True)

        st.write('친환경 자동차 등록현황 연도별 비교')
        chart_data1_1 = chart_data1[chart_data1['fuel'] == 'eco']
        st.bar_chart(chart_data1_1, x='year', y='num', stack=False)

    # Chart3
    chart_data2 = data1[data1['year'] == '2024']
    chart_data2_1 = chart_data2[chart_data2['fuel'].isin(eco_fuel)]
    chart_data2_1 = chart_data2_1.groupby('region')['count'].sum()

    chart_data2_2 = pd.DataFrame({
        '지역': chart_data2_1.index[1:],
        '등록현황': chart_data2_1.values[1:] / 10
    })
    chart_data2_2 = pd.merge(chart_data2_2, coordinate)

    st.write('2024년 지역별 친환경 자동차 등록 현황')

    st.map(chart_data2_2, latitude="위도", longitude="경도", size="등록현황")

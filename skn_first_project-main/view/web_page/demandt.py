import os
import sys
import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fetch_data_from_mysql():
    conn = mysql.connector.connect(
        host ="localhost",
        user = "team2",
        password = "team2",
        database = "team2"
    )

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, brand, fuel_type, car_type, car_name, elect_yn FROM kgmobility_car_info_data")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_sales_info():
    conn = mysql.connector.connect(
        host ="localhost",
        user = "team2",
        password = "team2",
        database = "team2"
    )

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM kgmobility_car_sales_data")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def run():
    st.title("📈 수요 분석")
    st.markdown("""
    ### 주요 5사 수요 트렌드
    국내 주요 5대 자동차 제조사의 친환경 자동차 수요 데이터를 분석합니다.
    """)

    st.info("💡 월별 수요 데이터와 수요 비중을 확인할 수 있습니다.")

    data = fetch_data_from_mysql()
    data2 = get_sales_info()

    df = pd.DataFrame(data, columns=["id", "brand", "fuel_type", "car_type", "car_name", "elect_yn"])

    st.write("### KGMobility Normal/EV Model List")
    st.dataframe(df, width=1000)
    #st.table({"Model Name": model_list})

    # 데이터프레임 생성
    df = pd.DataFrame(data2)
    
    rec_sports_df = df[df['model_name'] == '렉스턴 스포츠'][['model_name', 'sale_month', 'sale_count']]
    sale_month_df = df[df['model_name'] == '티볼리'][['model_name', 'sale_month', 'sale_count']]
    new_tores_df = df[df['model_name'] == '더 뉴 토레스'][['model_name', 'sale_month', 'sale_count']]
    action_df = df[df['model_name'] == '액티언'][['model_name', 'sale_month', 'sale_count']]
    rec_sports_kan_df = df[df['model_name'] == '렉스턴 스포츠 칸'][['model_name', 'sale_month', 'sale_count']]
    rec_new_arena_df = df[df['model_name'] == '렉스턴 뉴 아레나'][['model_name', 'sale_month', 'sale_count']]
    torex_EVX_df = df[df['model_name'] == '토레스 EVX'][['model_name', 'sale_month', 'sale_count']]
    corando_df = df[df['model_name'] == '코란도'][['model_name', 'sale_month', 'sale_count']]
    corando_EV_df = df[df['model_name'] == '코란도 EV'][['model_name', 'sale_month', 'sale_count']]

    unique_sale_months = df['sale_month'].unique()
    car_chart_data = pd.DataFrame({"sale_month": unique_sale_months})

    # 각 모델별 sale_count를 추가
    models = [
        ("렉스턴 스포츠", rec_sports_df),
        ("티볼리", sale_month_df),
        ("더 뉴 토레스", new_tores_df),
        ("액티언", action_df),
        ("렉스턴 스포츠 칸", rec_sports_kan_df),
        ("렉스턴 뉴 아레나", rec_new_arena_df),
        ("토레스 EVX", torex_EVX_df),
        ("코란도", corando_df),
        ("코란도 EV", corando_EV_df)
    ]

    for model_name, model_df in models:
        # sale_month를 기준으로 병합 (left join)
        car_chart_data = car_chart_data.merge(
            model_df[['sale_month', 'sale_count']],
            on='sale_month',
            how='left'
        )
        # 컬럼 이름 변경
        car_chart_data.rename(columns={'sale_count': model_name}, inplace=True)

    # NaN 값이 있는 경우 0으로 채우기 (옵션)
    car_chart_data.fillna(0, inplace=True)

    car_chart_data.set_index('sale_month', inplace=True)

    st.write('### KGMobility Normal/EV SALES Trends')

    # fig, ax = plt.subplots(figsize=(12, 6))
    # car_chart_data.plot(kind='line', ax=ax)

    # ax.set_xticklabels(car_chart_data.index, rotation=45)

    # ax.set_title('KGMobility Monthly Trend')
    # ax.set_xlabel('Sales Month')
    # ax.set_ylabel('Sales Count')

    # st.pyplot(fig)
    st.line_chart(car_chart_data)
    #st.pyplot(plot_monthly_trends(car_chart_data, title="KGMobility Monthly Trends"))

    # model_list, monthly_sales = process_hundae_data(sheet_name="Unit Sales by Model")

    # if model_list and monthly_sales is not None:
    #     # HEV/EV 모델 리스트 표시
    #     st.write("### Hyundai HEV/EV Model List")
    #     st.table({"Model Name": model_list})

    #     # 월별 데이터 시각화
    #     st.write("### Monthly Eco-friendly Vehicle Demand Trends")
    #     st.pyplot(plot_monthly_trends(monthly_sales, title="Hyundai Monthly Trends"))

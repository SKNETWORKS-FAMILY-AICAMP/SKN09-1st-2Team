import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from view.utils.file_loader import load_excel
from view.utils.data_refactoring import filter_hev_ev
import streamlit as st
from view.components.chart import plot_monthly_trends
from view.database.read.hyundai_data_read import fetch_car_sales_data
import matplotlib.pyplot as plt


def process_brand_data(car_sales_data, brand_name):
    """
    Process data for a specific brand.
    """
    brand_data = car_sales_data[car_sales_data['brand'] == brand_name]
    if brand_data.empty:
        return [], None

    # 모델 리스트와 월별 판매 데이터를 가공
    model_list = brand_data['model_name'].unique().tolist()
    monthly_sales = brand_data.pivot_table(
        index="model_name",
        columns="sale_month",
        values="sale_count",
        aggfunc="sum"
    )
    return model_list, monthly_sales


def process_hyundai_data(sheet_name="Unit Sales by Model"):
    """
    Load car sales data from Excel or database and process for all brands.
    """
    try:
        # 데이터베이스에서 데이터 가져오기
        mysql_host = "localhost"
        mysql_user = "root"
        mysql_password = "1234"
        mysql_database = "carsystemdb"
        car_sales_data = fetch_car_sales_data(mysql_host, mysql_user, mysql_password, mysql_database)

        if car_sales_data.empty:
            # Excel 데이터 로드
            data = load_excel(sheet_name=sheet_name, file_name="car_sales.xlsx", header=2)
            car_sales_data = data  # Excel 데이터를 사용할 경우 필요한 처리 추가 가능

        # 브랜드 리스트 가져오기
        brand_list = car_sales_data['brand'].unique().tolist()

        # 모든 브랜드에 대해 데이터 처리
        brand_data = {}
        for brand_name in brand_list:
            model_list, monthly_sales = process_brand_data(car_sales_data, brand_name)
            brand_data[brand_name] = {
                "model_list": model_list,
                "monthly_sales": monthly_sales
            }

        return brand_data

    except FileNotFoundError:
        return {}


def calculate_detailed_ev_hev_share(monthly_sales):
    """
    Calculate the detailed share of EV, HEV, and others in total sales.
    """
    total_sales = monthly_sales.sum().sum()
    ev_sales = monthly_sales.loc[monthly_sales.index.str.contains("EV", na=False)].sum().sum()
    hev_sales = monthly_sales.loc[monthly_sales.index.str.contains("HEV", na=False)].sum().sum()
    other_sales = total_sales - (ev_sales + hev_sales)

    # 음수 값 방지
    ev_sales = max(ev_sales, 0)
    hev_sales = max(hev_sales, 0)
    other_sales = max(other_sales, 0)

    return ev_sales, hev_sales, other_sales, total_sales


def render_ev_hev_share_pie_chart(ev_sales, hev_sales, other_sales):
    """
    Render a pie chart with EV, HEV, and Other sales share.
    """
    labels = ["EV (Electric Vehicle)", "HEV (Hybrid Electric Vehicle)", "Other"]
    sizes = [ev_sales, hev_sales, other_sales]

    # 합이 0인지 확인
    if sum(sizes) == 0:
        sizes = [1, 1, 1]  # 모든 값이 0일 경우 임시로 균등 분배

    explode = (0.1, 0.1, 0)  # EV와 HEV를 강조
    colors = ["#4CAF50", "#2196F3", "#FFC107"]

    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        autopct=lambda p: f"{p:.1f}%\n({int(p * sum(sizes) / 100):,})",
        startangle=90,
        colors=colors,
    )
    ax.axis("equal")  # 원형 유지
    ax.set_title("EV + HEV vs. Other Vehicles Share", fontsize=16)
    return fig


def calculate_fossil_vs_green_share(monthly_sales):
    """
    Calculate the share of fossil fuel cars vs green cars (EV + HEV).
    """
    total_sales = monthly_sales.sum().sum()
    ev_sales = monthly_sales.loc[monthly_sales.index.str.contains("EV", na=False)].sum().sum()
    hev_sales = monthly_sales.loc[monthly_sales.index.str.contains("HEV", na=False)].sum().sum()
    green_sales = ev_sales + hev_sales
    fossil_sales = total_sales - green_sales

    # 음수 값 방지
    green_sales = max(green_sales, 0)
    fossil_sales = max(fossil_sales, 0)

    return green_sales, fossil_sales


def render_fossil_vs_green_pie_chart(green_sales, fossil_sales):
    """
    Render a pie chart for fossil fuel vs green cars.
    """
    labels = ["Green Cars (EV + HEV)", "Fossil Fuel Cars"]
    sizes = [green_sales, fossil_sales]
    colors = ["#4CAF50", "#FF5722"]  # Green and Fossil Fuel colors

    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct=lambda p: f"{p:.1f}%\n({int(p * sum(sizes) / 100):,})",
        startangle=90,
        colors=colors,
    )
    ax.axis("equal")  # 원형 유지
    ax.set_title("Fossil Fuel vs. Green Cars Share", fontsize=16)
    return fig


def render_brand_analysis(brand_name, brand_data):
    """
    Render analysis for a specific brand.
    """
    st.subheader(f"{brand_name} 자동차")
    brand_info = brand_data.get(brand_name, {})
    model_list = brand_info.get("model_list", [])
    monthly_sales = brand_info.get("monthly_sales", None)

    if model_list and monthly_sales is not None:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"#### 친환경 자동차 리스트")
            st.markdown(
                """
                <style>
                .scrollable-container {
                    overflow-y: auto;
                    height: 400px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 10px;
                }
                .card {
                    padding: 10px;
                    margin-bottom: 10px;
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    font-size: 14px;
                    font-weight: bold;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            styled_cards = "<div class='scrollable-container'>"
            for model in model_list:
                styled_cards += f"<div class='card'>🚗 {model}</div>"
            styled_cards += "</div>"
            st.markdown(styled_cards, unsafe_allow_html=True)

        # 월별 수요 데이터 시각화
        with col2:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
                    <h4 style="text-align: center;">2023년 {brand_name} 월별 친환경 자동차 수요</h4>
                    <div>
                """,
                unsafe_allow_html=True,
            )
            st.pyplot(plot_monthly_trends(monthly_sales, title=f"{brand_name} Monthly Trends"))
            st.markdown("</div></div>", unsafe_allow_html=True)

        # 친환경 자동차와 화석 연료 자동차 비율 계산
        ev_sales, hev_sales, other_sales, total_sales = calculate_detailed_ev_hev_share(monthly_sales)

        # Fossil vs Green Cars 비율 계산
        green_sales, fossil_sales = calculate_fossil_vs_green_share(monthly_sales)

        # 두 개의 원 그래프를 가로로 나란히 표시
        st.markdown(f"### {brand_name} 자동차 친환경 vs 화석 연료 비율")
        fig1 = render_ev_hev_share_pie_chart(ev_sales, hev_sales, other_sales)
        fig2 = render_fossil_vs_green_pie_chart(green_sales, fossil_sales)

        col3, col4 = st.columns(2)
        with col3:
            st.pyplot(fig1)
        with col4:
            st.pyplot(fig2)


def render_analysis_for_all_brands():
    """
    Render analysis for all brands in the data.
    """
    brand_data = process_hyundai_data(sheet_name="Unit Sales by Model")

    if not brand_data:
        st.error("No data available.")
        return

    for brand_name in brand_data.keys():
        render_brand_analysis(brand_name, brand_data)

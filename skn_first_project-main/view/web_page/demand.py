import os
import sys
import streamlit as st
from view.service.demand_process import process_hundae_data
from view.components.chart import plot_monthly_trends

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)


def run():
    st.title("📈 수요 분석")
    st.markdown("""
    ### 주요 5사 수요 트렌드
    국내 주요 5대 자동차 제조사의 친환경 자동차 수요 데이터를 분석합니다.
    """)

    st.info("💡 월별 수요 데이터와 수요 비중을 확인할 수 있습니다.")

    model_list, monthly_sales = process_hundae_data(sheet_name="Unit Sales by Model")

    if model_list and monthly_sales is not None:
        # HEV/EV 모델 리스트 표시
        st.write("### Hyundai HEV/EV Model List")
        st.table({"Model Name": model_list})

        # 월별 데이터 시각화
        st.write("### Monthly Eco-friendly Vehicle Demand Trends")
        st.pyplot(plot_monthly_trends(monthly_sales, title="Hyundai Monthly Trends"))

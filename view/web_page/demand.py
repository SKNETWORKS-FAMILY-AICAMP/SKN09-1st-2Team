import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from view.service.hyundai_analysis import render_brand_analysis, process_hyundai_data


def run():
    st.title("📈 수요 분석")
    st.markdown("""
    ### 주요 5사 수요 트렌드
    국내 주요 5대 자동차 제조사의 친환경 자동차 수요 데이터를 분석합니다.
    """)

    st.info("💡 월별 수요 데이터와 수요 비중을 확인할 수 있습니다.")

    # 데이터 로드 및 브랜드 목록 가져오기
    brand_data = process_hyundai_data(sheet_name="Unit Sales by Model")
    if not brand_data:
        st.error("데이터를 불러오는 데 실패했습니다. 데이터베이스를 확인하세요.")
        return

    brand_list = list(brand_data.keys())
    selected_brand = st.selectbox("분석할 브랜드를 선택하세요:", brand_list)

    if selected_brand:
        render_brand_analysis(selected_brand, brand_data)

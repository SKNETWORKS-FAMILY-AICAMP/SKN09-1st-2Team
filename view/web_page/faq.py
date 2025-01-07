import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from view.utils.data_refactoring import make_dataframe

def run():
    st.title("❓ 자주 묻는 질문 FAQ")

    st.markdown(
        """
        <style>
        .pagination-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
        }
        .pagination-button {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            color: #333;
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .pagination-button:hover {
            background-color: #e0e0e0;
        }
        .pagination-button:disabled {
            background-color: #f2f2f2;
            color: #aaa;
            cursor: not-allowed;
        }
        .page-info {
            text-align: center;
            font-size: 14px;
        }
        .gray-box {
            background-color: #f2f2f2;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    faq_data = make_dataframe()

    if faq_data.empty:
        st.warning("FAQ 데이터를 로드하지 못했습니다.")
        return

    st.subheader("브랜드 선택")
    brands = ["전체"] + list(faq_data["brand"].unique())
    selected_brand = st.selectbox("브랜드를 선택하세요:", brands)

    if selected_brand != "전체":
        faq_data = faq_data[faq_data["brand"] == selected_brand]

    search_query = st.text_input("궁금하신 키워드를 검색하세요:")

    st.subheader("카테고리 선택")
    categories = ["전체"] + list(faq_data["category"].unique())
    selected_category = st.radio("카테고리를 선택하세요:", categories, horizontal=True)

    if (
        "previous_category" not in st.session_state
        or st.session_state.previous_category != selected_category
        or st.session_state.previous_brand != selected_brand
        or st.session_state.previous_query != search_query
    ):
        st.session_state.current_page = 1
        st.session_state.previous_category = selected_category
        st.session_state.previous_brand = selected_brand
        st.session_state.previous_query = search_query

    if selected_category != "전체":
        faq_data = faq_data[faq_data["category"] == selected_category]

    if search_query:
        faq_data = faq_data[
            faq_data["question"].str.contains(search_query, case=False, na=False) |
            faq_data["answer"].str.contains(search_query, case=False, na=False)
        ]

    st.subheader(f"질문 목록 ({len(faq_data)}개)")
    if not faq_data.empty:
        items_per_page = 10

        total_pages = (len(faq_data) - 1) // items_per_page + 1
        start_idx = (st.session_state.current_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_data = faq_data.iloc[start_idx:end_idx]

        for index, row in current_data.iterrows():
            with st.expander(f"❓ {row['question']}"):
                st.markdown(
                    f'<div class="gray-box">{row["answer"]}</div>',
                    unsafe_allow_html=True,
                )

        col1, col2, col3 = st.columns([1, 8, 1])

        with col1:
            if st.button("이전", key="prev", disabled=(st.session_state.current_page == 1)):
                st.session_state.current_page -= 1

        with col3:
            if st.button("다음", key="next", disabled=(st.session_state.current_page == total_pages)):
                st.session_state.current_page += 1

        with col2:
            st.markdown(
                f"<div class='page-info'>페이지 {st.session_state.current_page} / {total_pages}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("검색 결과가 없습니다.")

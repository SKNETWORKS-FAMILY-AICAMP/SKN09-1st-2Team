import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

st.set_page_config(
    page_title="친환경 자동차 현황",
    page_icon="🚗",
    layout="wide"
)

import view.web_page.registration as registration
import web_page.demand as demand
import web_page.faq as faq
import web_page.home as home

st.sidebar.title("📂 MENU")
menu = st.sidebar.radio(
    "페이지를 선택하세요:",
    ["🏠 Home", "📊 친환경 자동차 등록 현황", "📈 국내 주요 5사 자동차 분석", "❓ FAQ"],
    key="main_menu"
)

if menu == "🏠 Home":
    home.run()
elif menu == "📊 친환경 자동차 등록 현황":
    registration.run()
elif menu == "📈 국내 주요 5사 자동차 분석":
    demand.run()
elif menu == "❓ FAQ":
    faq.run()
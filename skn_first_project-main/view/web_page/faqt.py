import streamlit as st
import mysql.connector
import pandas as pd

def fetch_data_from_mysql():
    conn = mysql.connector.connect(
        host ="localhost",
        user = "team2",
        password = "team2",
        database = "team2"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT id, brand, category, question, answer FROM kgmobility_faq_data")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def run():
    st.title("❓ FAQ (자주 묻는 질문)")
    st.markdown("""
    ### 친환경 자동차 관련 FAQ 모음
    친환경 자동차에 대한 자주 묻는 질문과 답변을 제공합니다.
    """)

    st.info("💬 궁금한 점이 있다면 FAQ를 통해 확인하세요")

    data = fetch_data_from_mysql()

    df = pd.DataFrame(data, columns=["id", "brand", "category", "question", "answer"])
    
    st.write("KG모빌리티 데이터")
    st.dataframe(df)
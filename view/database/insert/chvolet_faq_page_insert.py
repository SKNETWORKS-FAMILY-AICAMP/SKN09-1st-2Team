import pandas as pd
import mysql.connector
from mysql.connector import Error


# MySQL 연결 및 데이터 삽입 함수
def insert_faq_data_to_mysql(csv_file_path, host, user, password, database):
    try:
        # CSV 파일 읽기
        faq_data = pd.read_csv(csv_file_path)

        # MySQL 연결
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")

        cursor = connection.cursor()

        # 데이터 삽입 쿼리
        insert_query = """
        INSERT INTO faq_data (brand, category, question, answer)
        VALUES (%s, %s, %s, %s)
        """

        # 데이터 삽입
        for _, row in faq_data.iterrows():
            cursor.execute(insert_query, (row['brand'], row['category'], row['question'], row['answer']))

        connection.commit()
        print("FAQ data inserted successfully into faq_data.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")


# 파일 경로와 MySQL 정보 설정
csv_file_path = r"C:\car_system\view\data\raw\chevrolet_faq_data.csv"  # CSV 파일 경로 설정
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "1234"
mysql_database = "carsystemdb"

try:
    # 데이터 삽입 함수 호출
    insert_faq_data_to_mysql(csv_file_path, mysql_host, mysql_user, mysql_password, mysql_database)

except Exception as e:
    print(f"Error processing CSV file: {e}")

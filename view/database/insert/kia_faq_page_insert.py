import mysql.connector
import pandas as pd
from kia_faq_dataframe import kia_faq_dataframe

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = "carsystemdb"
)

if connection.is_connected():
    print("MySQL에 성공적으로 연결되었습니다.")

cursor = connection.cursor()

sql = "INSERT INTO faq_data(brand, category, question, answer) VALUES(%s, %s, %s, %s)" # %S place holder 는 자리를 잡고 있는 것들 이라는 의미

for i, row in kia_faq_dataframe.iterrows():
    values = (row['brand'], row['category'], row['question'], row['answer'] ) # 순서대로

    cursor.execute(sql, values) # 넣긴했지만 해당 사항을 반영하지 않고 끊어진 것 , # 오토인크리어블의 단점
    connection.commit() # 작업을 공용 데이터 베이스에 올리게 된다.

cursor.close()
connection.close() # 이렇게 연결을 열었으면 반드시 닫아줘야 함
# 코드가 좋은 이유 = 내 논리를 구현시킬 수 있다.
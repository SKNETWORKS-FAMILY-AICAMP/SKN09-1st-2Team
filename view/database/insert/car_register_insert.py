import mysql.connector
import csv

with open("../../data/raw/whole_car_regist.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    data = list(reader)

# MySQL 연결
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="carsystemdb"
)

if connection.is_connected():
    print("MYSQL에 성공적으로 연결되었습니다.")

cursor = connection.cursor()


# 데이터 삽입
for row in data[1:]:
    sql = "INSERT INTO car_reg_info(regist_date, region, fuel_type, region_regist) VALUES (%s, %s, %s, %s)"
    print(row)
    values = (row[2], row[4], row[3], row[5])
    cursor.execute(sql, values)
    connection.commit()

cursor.close()
connection.close()

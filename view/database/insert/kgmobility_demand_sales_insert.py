import mysql.connector
import csv

# month를 딕셔너리
month = {
    "01": "Jan.", "02": "Feb.", "03": "Mar.", "04": "Apr.", "05": "May.",
    "06": "Jun.", "07": "Jul.", "08": "Aug.", "09": "Sep.", "10": "Oct.",
    "11": "Nov.", "12": "Dec."
}

# 브랜드 이름을 한글에서 영어로 변환하는 딕셔너리 (Hyundai와 KGM 제외)
brand_translation = {
    "기아": "Kia",
    "쉐보레": "Chevrolet",
    "르노코리아": "Renault Korea"
}

# CSV 파일을 읽어서 데이터 로드
with open("../../data/raw/car_sales_data.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    data = list(reader)

print(data)

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

# 데이터 삽입 SQL
sql = "INSERT INTO car_sales_data(brand, fuel_name, model_name, sale_month, sale_count) VALUES (%s, %s, %s, %s, %s)"

# 데이터 삽입
for row in data[1:]:
    if row[0] in brand_translation:  # Hyundai와 KGM을 제외
        brand = brand_translation[row[0]]
        sale_month = month[row[1]]
        if row[4]:
            row[4] = int(row[4].replace(',', ''))  # Remove commas and convert to integer
        else:
            row[4] = 0  # Or set to a default value like 0 if empty
        values = (brand, row[3], row[2], sale_month, row[4])  # Optional, to verify the values you're inserting
        cursor.execute(sql, values)
        connection.commit()

cursor.close()
connection.close()

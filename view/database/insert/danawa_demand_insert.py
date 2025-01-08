import mysql.connector
import csv

month = {
    "01": "Jan.", "02": "Feb.", "03": "Mar.", "04": "Apr.", "05": "May.",
    "06": "Jun.", "07": "Jul.", "08": "Aug.", "09": "Sep.", "10": "Oct.",
    "11": "Nov.", "12": "Dec."
}

brand_translation = {
    "현대": "Hyundai",
    "기아": "Kia",
    "쉐보레": "Chevrolet",
    "KGM": "KGM",
    "르노코리아": "Renault Korea"
}

with open("../../data/raw/car_sales_data.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    data = list(reader)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="carsystemdb"
)

if connection.is_connected():
    print("MYSQL에 성공적으로 연결되었습니다.")

cursor = connection.cursor()

sql = "INSERT INTO car_sales_data(brand, fuel_name, model_name, sale_month, sale_count) VALUES (%s, %s, %s, %s, %s)"

for row in data[1:]:
    if row[0] in ['현대', 'KGM']:
        continue

    brand = brand_translation.get(row[0], row[0])
    sale_month = month[row[1]]
    if row[4]:
        row[4] = int(row[4].replace(',', ''))
    else:
        row[4] = 0
    values = (brand, row[3], row[2], sale_month, row[4])
    cursor.execute(sql, values)
    connection.commit()

cursor.close()
connection.close()

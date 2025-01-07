import pandas as pd
import mysql.connector
from mysql.connector import Error

def filter_hev_ev(data: pd.DataFrame, model_column: str = "Unnamed: 2", month_start: str = "Jan.", month_end: str = "Dec."):
    data_fixed = data.drop(columns=["Unnamed: 0", "Unnamed: 1"], errors="ignore")
    filtered_data = data_fixed[data_fixed[model_column].str.contains("HEV|EV", na=False, case=False)]
    model_list = filtered_data[model_column].tolist()
    monthly_data = filtered_data.loc[:, month_start:month_end].apply(pd.to_numeric, errors="coerce")
    monthly_data.index = filtered_data[model_column]

    return model_list, monthly_data

def insert_data_to_mysql(data, host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")

        cursor = connection.cursor()

        # 기존 데이터를 삭제하고 AUTO_INCREMENT 초기화
        truncate_query = "TRUNCATE TABLE car_info_data"
        cursor.execute(truncate_query)
        print("Table car_info_data has been truncated (data deleted and AUTO_INCREMENT reset).")

        # 새 데이터를 삽입
        insert_query = """
        INSERT INTO car_info_data (brand, fuel_type, car_type, car_name, elect_yn)
        VALUES (%s, %s, %s, %s, %s)
        """

        for car_name in data.index:
            if "HEV" in car_name:
                fuel_type = "Hybrid"
                elect_yn = "Y"
            elif "EV" in car_name:
                fuel_type = "Electric"
                elect_yn = "Y"
            else:
                fuel_type = "Gasoline"
                elect_yn = "N"

            brand = "Hyundai"
            car_type = "RV" if "RV" in car_name else "Other"
            cursor.execute(insert_query, (brand, fuel_type, car_type, car_name, elect_yn))

        connection.commit()
        print("Data inserted successfully into car_info_data.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

# 파일 경로와 MySQL 정보 설정
excel_file_path = r"C:\car_system\view\data\raw\hyundai_demand.xlsx"
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "1234"
mysql_database = "carsystemdb"

try:
    # Excel 데이터 읽기
    excel_data = pd.read_excel(excel_file_path, skiprows=2)  # 헤더를 확인 후 적절히 설정
    model_list, monthly_data = filter_hev_ev(excel_data)

    # 전처리된 데이터를 MySQL에 삽입
    if not monthly_data.empty:
        insert_data_to_mysql(monthly_data, mysql_host, mysql_user, mysql_password, mysql_database)

except Exception as e:
    print(f"Error processing Excel file: {e}")

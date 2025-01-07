import pandas as pd
import mysql.connector
from mysql.connector import Error

def process_car_sales(data: pd.DataFrame, model_column: str = "Unnamed: 2", month_start: str = "Jan.", month_end: str = "Dec."):
    data_fixed = data.drop(columns=["Unnamed: 0", "Unnamed: 1"], errors="ignore")

    data_fixed[model_column] = data_fixed[model_column].fillna("").astype(str)

    def extract_fuel_type(model_name):
        if "HEV" in model_name:
            return "Hybrid"
        elif "PHEV" in model_name:
            return "Plug-in Hybrid"
        elif "EV" in model_name:
            return "Electric"
        else:
            return "Gasoline"

    data_fixed["fuel_name"] = data_fixed[model_column].apply(extract_fuel_type)

    # 월별 데이터를 int로 변환
    monthly_data = data_fixed.loc[:, month_start:month_end].apply(pd.to_numeric, errors="coerce").fillna(0)
    monthly_data = monthly_data.astype(int)  # float을 int로 변환

    model_list = data_fixed[model_column].tolist()
    monthly_data.index = data_fixed[model_column]

    return data_fixed, model_list, monthly_data

def insert_car_sales_data_to_mysql(data, monthly_data, model_column, host, user, password, database):
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

        truncate_query = "TRUNCATE TABLE car_sales_data"
        cursor.execute(truncate_query)
        print("Table car_sales_data has been truncated (data deleted and AUTO_INCREMENT reset).")

        insert_query = """
        INSERT INTO car_sales_data (brand, fuel_name, model_name, sale_month, sale_count)
        VALUES (%s, %s, %s, %s, %s)
        """

        for model_name in monthly_data.index:
            if not model_name.strip():
                continue

            fuel_name_row = data.loc[data[model_column] == model_name, "fuel_name"]

            if fuel_name_row.empty:
                fuel_name = "Unknown"  # 데이터가 없을 경우 기본값
            else:
                fuel_name = fuel_name_row.iloc[0]

            for sale_month, sale_count in monthly_data.loc[model_name].items():
                if isinstance(sale_count, (int, float)) and sale_count > 0:  # sale_count가 숫자인지 확인
                    cursor.execute(insert_query, ("Hyundai", fuel_name, model_name, sale_month, sale_count))

        connection.commit()
        print("Car sales data inserted successfully.")

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
    excel_data = pd.read_excel(excel_file_path, skiprows=2)
    model_column = "Unnamed: 2"  # 모델 이름이 있는 열
    processed_data, model_list, monthly_data = process_car_sales(excel_data, model_column=model_column)

    if not monthly_data.empty:
        insert_car_sales_data_to_mysql(processed_data, monthly_data, model_column, mysql_host, mysql_user, mysql_password, mysql_database)

except Exception as e:
    print(f"Error processing Excel file: {e}")

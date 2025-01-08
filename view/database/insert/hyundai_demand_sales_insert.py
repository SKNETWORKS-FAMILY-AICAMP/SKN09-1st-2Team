import pandas as pd
import mysql.connector
from mysql.connector import Error

def process_car_sales(data: pd.DataFrame, model_column: str = "Unnamed: 2", month_start: str = "Jan.", month_end: str = "Dec."):
    """
    Process the car sales data and prepare for database insertion.
    """
    # 불필요한 열 제거
    print("Dropping unnecessary columns...")
    data_fixed = data.drop(columns=["Unnamed: 0", "Unnamed: 1"], errors="ignore")

    # 모델 이름이 비어있지 않도록 처리
    print("Filling missing model names...")
    data_fixed[model_column] = data_fixed[model_column].fillna("").astype(str)

    # 총계, 소계 등 불필요한 행 제거
    valid_data = data_fixed[
        ~data_fixed[model_column].str.strip().isin(["", "Sub-total", "Total", "Grand Total"])
    ]

    # 연료 유형 추출
    def extract_fuel_type(model_name):
        if "HEV" in model_name:
            return "Hybrid"
        elif "PHEV" in model_name:
            return "Plug-in Hybrid"
        elif "EV" in model_name:
            return "Electric"
        else:
            return "Fossil Fuel"  # 기본 연료 유형

    valid_data["fuel_name"] = valid_data[model_column].apply(extract_fuel_type)

    # 월별 데이터를 숫자로 변환
    print("Converting monthly sales data to numeric values...")
    monthly_data = valid_data.loc[:, month_start:month_end].apply(pd.to_numeric, errors="coerce").fillna(0)
    monthly_data = monthly_data.astype(int)  # float을 int로 변환

    # 모델 리스트 생성
    model_list = valid_data[model_column].tolist()
    monthly_data.index = valid_data[model_column]

    print("Processed monthly data:")
    print(monthly_data.head())

    return valid_data, model_list, monthly_data

def insert_car_sales_data_to_mysql(data, monthly_data, model_column, host, user, password, database):
    """
    Insert the processed car sales data into MySQL database.
    """
    try:
        # MySQL 연결
        print("Connecting to MySQL database...")
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")

        cursor = connection.cursor()

        # 테이블 초기화
        truncate_query = "TRUNCATE TABLE car_sales_data"
        cursor.execute(truncate_query)
        print("Table car_sales_data has been truncated (data deleted and AUTO_INCREMENT reset).")

        # 데이터 삽입 쿼리
        insert_query = """
        INSERT INTO car_sales_data (brand, fuel_name, model_name, sale_month, sale_count)
        VALUES (%s, %s, %s, %s, %s)
        """

        # 데이터 삽입
        print("Inserting data into MySQL...")
        for model_name, row in monthly_data.iterrows():
            if not model_name.strip():
                print(f"Skipping empty model name: {model_name}")
                continue

            # 연료 유형 가져오기
            fuel_name_row = data.loc[data[model_column] == model_name, "fuel_name"]
            fuel_name = fuel_name_row.iloc[0] if not fuel_name_row.empty else "Unknown"

            # 월별 데이터 삽입
            for sale_month, sale_count in row.items():
                if sale_count > 0:  # 판매량이 0 이상인 경우에만 삽입
                    print(f"Inserting {model_name} - {fuel_name} - {sale_month}: {sale_count}")
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
    # 엑셀 데이터 로드
    print("Reading Excel file...")
    excel_data = pd.read_excel(excel_file_path, skiprows=2)
    model_column = "Unnamed: 2"  # 모델 이름이 있는 열

    # 데이터 처리
    print("Processing car sales data...")
    processed_data, model_list, monthly_data = process_car_sales(excel_data, model_column=model_column)

    # 데이터 삽입
    if not monthly_data.empty:
        print("Inserting processed data into MySQL...")
        insert_car_sales_data_to_mysql(processed_data, monthly_data, model_column, mysql_host, mysql_user, mysql_password, mysql_database)

except FileNotFoundError:
    print(f"Error: Excel file not found at {excel_file_path}.")
except Exception as e:
    print(f"Error processing Excel file: {e}")

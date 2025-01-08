import pandas as pd
import mysql.connector
from mysql.connector import Error


def process_car_sales(data: pd.DataFrame, model_column: str = "Unnamed: 2", month_start: str = "Jan.",
                      month_end: str = "Dec."):
    """
    Process car sales data, including all car types.
    """
    print("Dropping unnecessary columns...")
    data_fixed = data.drop(columns=["Unnamed: 0", "Unnamed: 1"], errors="ignore")

    print("Filling missing model names...")
    data_fixed[model_column] = data_fixed[model_column].fillna("").astype(str)
    print(f"Sample model names after fillna: {data_fixed[model_column].head()}")

    print("Filtering valid models (excluding 'Sub-total', 'Total', 'Grand Total')...")
    valid_data = data_fixed[
        ~data_fixed[model_column].str.strip().isin(["", "Sub-total", "Total", "Grand Total"])
    ]
    print(f"Filtered valid models: {valid_data[model_column].tolist()}")

    print("Converting monthly sales data to numeric values...")
    monthly_data = valid_data.loc[:, month_start:month_end].apply(pd.to_numeric, errors="coerce").fillna(0)
    monthly_data = monthly_data.astype(int)
    monthly_data.index = valid_data[model_column]

    print("Processed monthly data:")
    print(monthly_data.head())

    return valid_data, monthly_data


def insert_data_to_mysql(data, monthly_data, model_column, host, user, password, database):
    """
    Insert all car sales data into MySQL, including all car types.
    """
    try:
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

        print("Truncating car_info_data table...")
        truncate_query = "TRUNCATE TABLE car_info_data"
        cursor.execute(truncate_query)
        print("Table car_info_data has been truncated (data deleted and AUTO_INCREMENT reset).")

        insert_query = """
        INSERT INTO car_info_data (brand, fuel_type, car_type, car_name, elect_yn)
        VALUES (%s, %s, %s, %s, %s)
        """

        print("Inserting data into MySQL...")
        for model_name, row in monthly_data.iterrows():
            if not model_name.strip():
                print(f"Skipping empty model name: {model_name}")
                continue

            fuel_type = "Fossil Fuel"
            elect_yn = "N"
            if "HEV" in model_name:
                fuel_type = "Hybrid"
                elect_yn = "Y"
            elif "PHEV" in model_name:
                fuel_type = "Plug-in Hybrid"
                elect_yn = "Y"
            elif "EV" in model_name:
                fuel_type = "Electric"
                elect_yn = "Y"

            brand = "Hyundai"
            car_type = "RV" if "RV" in model_name else "Other"

            for sale_month, sale_count in row.items():
                if isinstance(sale_count, (int, float)) and sale_count > 0:  # sale_count가 숫자인지 확인
                    print(f"Inserting {model_name} - {fuel_type} - {sale_month}: {sale_count}")
                    cursor.execute(insert_query, (brand, fuel_type, car_type, model_name, elect_yn))

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
    print("Reading Excel file...")
    excel_data = pd.read_excel(excel_file_path, skiprows=2)
    print("Excel file read successfully.")

    print("Processing car sales data...")
    model_column = "Unnamed: 2"
    processed_data, monthly_sales = process_car_sales(excel_data, model_column=model_column)
    print(f"Processed data for models: {processed_data[model_column].tolist()}")

    if not monthly_sales.empty:
        print("Inserting processed data into MySQL...")
        insert_data_to_mysql(processed_data, monthly_sales, model_column, mysql_host, mysql_user, mysql_password,
                             mysql_database)

except FileNotFoundError:
    print(f"Error: Excel file not found at {excel_file_path}.")
except ValueError as ve:
    print(f"Error processing data: {ve}")
except Exception as e:
    print(f"Error: {e}")

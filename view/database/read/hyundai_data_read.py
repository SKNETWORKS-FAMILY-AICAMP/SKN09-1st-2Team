import pandas as pd
import mysql.connector
from mysql.connector import Error


def fetch_car_sales_data(host, user, password, database, table_name="car_sales_data"):
    """
    Fetch data from the specified MySQL table and return as a pandas DataFrame.

    Parameters:
    - host: str, MySQL host
    - user: str, MySQL user
    - password: str, MySQL password
    - database: str, MySQL database name
    - table_name: str, MySQL table name (default: 'car_sales_data')

    Returns:
    - pandas.DataFrame containing the fetched data
    """
    try:
        # MySQL 연결
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")

            # SQL 쿼리 실행
            query = f"SELECT * FROM {table_name}"
            print(f"Executing query: {query}")

            # pandas를 사용해 데이터를 읽어옴
            data = pd.read_sql(query, connection)

            return data

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return pd.DataFrame()  # 빈 데이터프레임 반환
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection closed.")


# MySQL 정보
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "1234"
mysql_database = "carsystemdb"

# 함수 호출
car_sales_data = fetch_car_sales_data(mysql_host, mysql_user, mysql_password, mysql_database)

# 결과 확인
if not car_sales_data.empty:
    print("Data fetched successfully!")
    print(car_sales_data.head())  # 데이터 일부 출력
else:
    print("No data fetched or table is empty.")

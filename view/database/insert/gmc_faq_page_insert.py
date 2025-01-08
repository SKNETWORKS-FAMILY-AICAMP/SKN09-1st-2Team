import pandas as pd
import mysql.connector
from mysql.connector import Error


def insert_faq_data_to_mysql(csv_file_path, host, user, password, database):
    try:
        faq_data = pd.read_csv(csv_file_path)

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")

        cursor = connection.cursor()

        insert_query = """
        INSERT INTO faq_data (brand, category, question, answer)
        VALUES (%s, %s, %s, %s)
        """

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


csv_file_path = r"C:\car_system\view\data\raw\gmc_faq_data.csv"
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "1234"
mysql_database = "carsystemdb"

try:
    insert_faq_data_to_mysql(csv_file_path, mysql_host, mysql_user, mysql_password, mysql_database)

except Exception as e:
    print(f"Error processing CSV file: {e}")

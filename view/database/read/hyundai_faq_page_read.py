import mysql.connector

def load_data_from_database():
    connection = mysql.connector.connect(
        host="localhost",
        user='root',
        password='1234',
        database='carsystemdb'
    )

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM faq_data")

    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows
import mysql.connector


# 일단 월별 데이터 다 받아와

def sql_read():
    connection = mysql.connector.connect(
        host="localhost",
        user="squirrel",
        password="squirrel",
        database="faqdb"  # 추후 다른 데이터 테이블 연결
    )

    if connection.is_connected():
        print("MySQL에 성공적으로 연결되었습니다.")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM yj_data")
    results = cursor.fetchall()

    # 데이터를 확인해 봄
    for row in results:
        print(f"id: {row[0]}, brand: {row[1]}, category: {row[2]}, question: {row[3]}, answer: {row[4]}")

    cursor.close()
    connection.close()

    print(results)

    return results


sql_read()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import time
import csv


def insert_data(sql, values):
    status = ''
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="carsystemdb"
    )

    cursor = conn.cursor()

    try:
        cursor.execute(sql, values)
        conn.commit()
        print("데이터 삽입 성공")
        status = 'success'

    except Exception as e:
        print("데이터 삽입 실패:", e)
        status = 'fail'
    finally:
        cursor.close()
        conn.close()

    return status


csv_file = open("../../data/raw/전성원_KGMobility_car_sales_data.csv", mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['brand', 'model_name', 'month', 'sale_count'])

driver = webdriver.Chrome()
driver.get('https://auto.danawa.com/auto/?Work=brand&Tab=record&Brand=326&pcUse=y')
time.sleep(2)

wait = WebDriverWait(driver, 10)

brand = 'kgmobility'

try:
    car_table = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.model tbody tr')))
    # = driver.find_elements(By.CSS_SELECTOR, '.model tbody tr')
    for ct in car_table:
        car_name = ct.find_element(By.CSS_SELECTOR, '.title a')
        print('차 이름:', car_name.text)

        car_sales_btn = ct.find_element(By.CSS_SELECTOR, '.num button')
        car_sales_btn.click()
        time.sleep(2)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#popup_data .recordMonth')))

        table = driver.find_element(By.CSS_SELECTOR, '#popup_data .recordMonth')

        header_cells = table.find_elements(By.CSS_SELECTOR, 'thead th')
        months = [header_cell.text for header_cell in header_cells if header_cell.text != '년월']

        # rows = driver.find_elements(By.CSS_SELECTOR, '.recordMonth tbody tr')

        body_cells = table.find_elements(By.CSS_SELECTOR, 'tbody tr td')
        sales_numbers = [body_cell.text for body_cell in body_cells if body_cell.text != '대수']

        for month, sales in zip(months, sales_numbers):
            if sales == '-':
                print(f"{month}: {0}")
                csv_writer.writerow([brand, car_name.text, str(month), 0])
            else:
                print(f"{month}: {sales}")
                if "," in sales:
                    csv_writer.writerow([brand, car_name.text, str(month), int(sales.replace(',', ''))])
                    sql = """
                        INSERT INTO car_sales_data (brand, model_name, sale_month, sale_count) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    values = (brand, car_name.text, str(month), int(sales.replace(',', '')))
                    insert_data(sql, values)
                else:
                    csv_writer.writerow([brand, car_name.text, str(month), sales])
                    sql = """
                        INSERT INTO car_sales_data (brand, model_name, sale_month, sale_count) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    values = (brand, car_name.text, str(month), sales)
                    insert_data(sql, values)

        close_btn = driver.find_element(By.CSS_SELECTOR, '.close')
        close_btn.click()

        time.sleep(2)

except Exception as e:
    print(f'오류 발생: {e}')
finally:
    csv_file.close()
    driver.quit()
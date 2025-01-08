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
        host ="localhost",
        user = "team2",
        password = "team2",
        database = "team2"
    )

    cursor = conn.cursor()

    try:
        cursor.execute(sql,values)
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

def switch_month(month):
    if "24.01" in month:
        month = "Jan."
    if "24.02" in month:
        month = "Feb."
    if "24.03" in month:
        month = "Mar."
    if "24.04" in month:
        month = "Apr."
    if "24.05" in month:
        month = "May."
    if "24.06" in month:
        month = "Jun."
    if "24.07" in month:
        month = "Jul."
    if "24.08" in month:
        month = "Aug."
    if "24.09" in month:
        month = "Sep."
    if "24.10" in month:
        month = "Oct."
    if "24.11" in month:
        month = "Nov."
    if "24.12" in month:
        month = "Dec."
    return month

csv_file = open("전성원_KGMobility_car_sales_data.csv", mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['brand', 'model_name', 'month', 'sale_count'])

driver = webdriver.Chrome()
driver.get('https://auto.danawa.com/auto/?Work=brand&Tab=record&Brand=326&pcUse=y')
time.sleep(2)

wait = WebDriverWait(driver, 10)

brand = 'kgmobility'

try:
    car_table = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.model tbody tr')))
    #= driver.find_elements(By.CSS_SELECTOR, '.model tbody tr')
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

        #rows = driver.find_elements(By.CSS_SELECTOR, '.recordMonth tbody tr')

        body_cells = table.find_elements(By.CSS_SELECTOR, 'tbody tr td')
        sales_numbers = [body_cell.text for body_cell in body_cells if body_cell.text != '대수']

        for month, sales in zip(months, sales_numbers):
            if '23.12' not in month:
                if sales == '-':
                    print(f"{month}: {0}")
                    csv_writer.writerow([brand, car_name.text, switch_month(str(month)), 0])
                    if car_name.text in ['코란도 EV', '토레스 EVX']:
                        print("전기")
                        sql = """
                            INSERT INTO car_sales_data (brand, fuel_name, model_name, sale_month, sale_count) 
                            VALUES (%s, %s, %s, %s, %s)
                        """
                        values = (brand, 'Electronic', car_name.text, switch_month(str(month)), 0)
                        insert_data(sql,values)
                    else:
                        sql = """
                            INSERT INTO car_sales_data (brand, fuel_name, model_name, sale_month, sale_count) 
                            VALUES (%s, %s, %s, %s, %s)
                        """
                        values = (brand, 'Fossil Fuel', car_name.text, switch_month(str(month)), 0)
                        insert_data(sql,values)
                else:
                    print(f"{month}: {sales}")
                    if "," in sales:
                        csv_writer.writerow([brand, car_name.text, switch_month(str(month)), int(sales.replace(',', ''))])
                        if car_name.text in ['코란도 EV', '토레스 EVX']:
                            print("전기")
                            sql = """
                                INSERT INTO car_sales_data (brand, fuel_name, model_name, sale_month, sale_count) 
                                VALUES (%s, %s, %s, %s, %s)
                            """
                            values = (brand, 'Electronic', car_name.text, switch_month(str(month)), int(sales.replace(',', '')))
                            insert_data(sql,values)
                        else:
                            sql = """
                                INSERT INTO car_sales_data (brand, fuel_name, model_name, sale_month, sale_count) 
                                VALUES (%s, %s, %s, %s, %s)
                            """
                            values = (brand, 'Fossil Fuel', car_name.text, switch_month(str(month)), int(sales.replace(',', '')))
                            insert_data(sql,values)
                    else:
                        csv_writer.writerow([brand, car_name.text, switch_month(str(month)), sales])
                        if car_name.text in ['코란도 EV', '토레스 EVX']:
                            print("전기")
                            sql = """
                                INSERT INTO car_sales_data (brand, fuel_name, model_name, sale_month, sale_count) 
                                VALUES (%s, %s, %s, %s, %s)
                            """
                            values = (brand, 'Electronic', car_name.text, switch_month(str(month)), sales)
                            insert_data(sql,values)
                        else:
                            sql = """
                                INSERT INTO car_sales_data (brand, fuel_name, model_name, sale_month, sale_count) 
                                VALUES (%s, %s, %s, %s, %s)
                            """
                            values = (brand, 'Fossil Fuel', car_name.text, switch_month(str(month)), sales)
                            insert_data(sql,values)

        close_btn = driver.find_element(By.CSS_SELECTOR, '.close')
        close_btn.click()
        
        time.sleep(2)
        
except Exception as e:
    print(f'오류 발생: {e}')
finally:
    csv_file.close()
    driver.quit()
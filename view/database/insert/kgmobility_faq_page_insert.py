from selenium import webdriver
from selenium.webdriver.common.by import By
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


category_code = [304, 305]  # 차량정비, 부품
category_map = {304: '차량정비', 305: '부품'}
driver = webdriver.Chrome()

# CSV 파일 설정
csv_file = open('전성원_KGMobility_faq_data.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['brand', 'category', 'question', 'answer'])


def crawl_page():
    question_btns = driver.find_elements(By.CLASS_NAME, 'accordion-header')

    for question_btn in question_btns:
        paragraphs = question_btn.find_elements(By.TAG_NAME, 'p')

        question = ''
        for p in paragraphs:
            class_attr = p.get_attribute('class')
            print('attr:', class_attr)
            if not class_attr:
                question = p.text
                break

        print(f"질문: {question}")

        question_btn.click()
        time.sleep(2)

        try:
            answer = driver.find_element(By.CLASS_NAME, 'custom-scroll-wrap')
            print(f"답변: {answer.text}")

            csv_writer.writerow(['kgmobility', category_map[category], question, answer.text])
            sql = """
                INSERT INTO faq_data (brand, category, question, answer) 
                VALUES (%s, %s, %s, %s)
            """
            values = ('kgmobility', category_map[category], question, answer.text)
            insert_data(sql, values)
        except Exception as e:
            print(f'답변을 찾을 수 없습니다: {e}')

        print("=" * 50)


for category in category_code:
    url = f"https://www.kg-mobility.com/sr/online-center/faq/detail?searchWord=&categoryCd={category}"
    driver.get(url)
    time.sleep(2)

    page_number = 1
    while True:
        print(f"크롤링 중: {page_number} 페이지")
        print(f"카테고리 코드: {category}")
        crawl_page()
        try:
            # //*[@id="app"]/div/div/div[2]/div/div/div/div[2]/div[3]/div/ul/li[3]/button
            next_page_btn = driver.find_element(By.XPATH,
                                                f'//*[@id="app"]/div/div/div[2]/div/div/div/div[2]/div[3]/div/ul/li[{3 + page_number}]/button')
            next_page_btn.click()
            time.sleep(2)
            page_number += 1
        except Exception as e:
            print(f"다음 페이지로 이동할 수 없습니다. 마지막 페이지입니다. ({e})")
            page_number = 0
            break

csv_file.close()

driver.quit()
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

# Chrome WebDriver 설정
driver = webdriver.Chrome()
driver.get('https://www.kg-mobility.com/pr/model')

# CSV 파일 설정
csv_file = open('전성원_KGMobility_car_info_data.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['brand', 'fuel_type', 'car_type', 'car_name', 'elect_yn'])

brand = 'kgmobility'

try:
    # 카테고리 버튼들이 로드될 때까지 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.swiper-wrapper a'))
    )
    
    # 초기 카테고리 버튼 목록 가져오기
    car_types = driver.find_elements(By.CSS_SELECTOR, '.swiper-wrapper a')
    num_categories = len(car_types)  # 총 카테고리 수 저장
    
    #for i in range(num_categories):
    # 각 반복마다 요소를 다시 찾아야 함
    car_types = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.swiper-wrapper a'))
    )
        
    # 카테고리 클릭 후 자동차 이름들이 로드될 때까지 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.name'))
    )
        
    # 자동차 이름과 링크 요소들 다시 가져오기
    car_names = driver.find_elements(By.CSS_SELECTOR, '.name')
    car_links = driver.find_elements(By.CSS_SELECTOR, '.estimate-button')
        
    num_cars = len(car_names)  # 각 카테고리 내 자동차 수 저장
        
    for j in range(num_cars):
        # 각 반복마다 요소를 다시 찾아야 함
        car_names = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.name'))
        )
        car_links = driver.find_elements(By.CSS_SELECTOR, '.estimate-button')
            
        car_name = car_names[j]
        car_link = car_links[j]
            
        if car_name.text not in ['렉스턴 써밋', '토레스 밴', '토레스 EVX 밴', '토레스 EVX 택시', '코란도 EV 택시', '토레스 바이퓨얼 택시', '렉스턴 스포츠 칸']:
            # 자동차 링크 클릭
            car_link.click()
                
            # 상세 페이지 로드 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.info-box'))
            )
                
            # 자동차 정보 가져오기
            car_infos = driver.find_elements(By.CSS_SELECTOR, '.info-box')
            for car_info in car_infos:
                label = car_info.find_element(By.CSS_SELECTOR, '.label').text
                title = car_info.find_element(By.CSS_SELECTOR, '.title').text
                car_ty = ''
                elect_yn = ''
                print('연료종류:', label)
                print('차 이름:', title)

                if title in ['렉스턴 스포츠 칸', '렉스턴 스포츠']:
                    print('차종: TRUCK')
                    car_ty='TRUCK'
                elif '밴' in title:
                    print('차종: VAN')
                    car_ty='VAN'
                else:
                    print('차종: SUV')
                    car_ty='SUV'

                if 'EV' in title or 'EVX' in title:
                    print('전기차여부: O')
                    elect_yn = 'Y'
                else:
                    print('전기차여부: X')
                    elect_yn = 'N'

                csv_writer.writerow([brand, label, car_ty, title, elect_yn])
                sql = """
                    INSERT INTO car_info_data (brand, fuel_type, car_type, car_name, elect_yn) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                values = (brand, label, car_ty, title, elect_yn)
                insert_data(sql,values)

                print('='*50)
                
            # 다시 이전 페이지로 돌아가기
            driver.back()
                
            # 이전 페이지가 로드될 때까지 대기
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.name'))
            )
            time.sleep(1)  # 추가적인 안정성을 위해 짧은 대기
        elif car_name.text not in ['토레스 밴', '토레스 EVX 밴', '렉스턴 스포츠 칸', '렉스턴 스포츠']:
            car_ty = ''
            elect_yn = ''
            fuel_type = ''
            print('차 이름:', car_name.text)
            if '밴' in car_name.text:
                print('차종: VAN')
                car_ty = 'VAN'
            elif '택시' in car_name.text:
                print('차종: TAXI')
                car_ty = 'TAXI'
            else:
                print('차종: SUV')
                car_ty = 'SUV'
                
            if 'EV' in car_name.text or 'EVX' in car_name.text:
                print('전기차여부: O')
                elect_yn = 'Y'
                fuel_type = '배터리'
            else:
                print('전기차여부: X')
                elect_yn = 'N'
                fuel_type = '가솔린'
            print('='*50)

            csv_writer.writerow([brand, fuel_type, car_ty, car_name.text, elect_yn])
            sql = """
                INSERT INTO car_info_data (brand, fuel_type, car_type, car_name, elect_yn) 
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (brand, label, car_ty, title, elect_yn)
            insert_data(sql,values)
        
    csv_file.close()
        
    # 카테고리 클릭 후 필요한 경우 다시 대기
    #time.sleep(1)

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    driver.quit()

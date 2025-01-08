import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def download_hyundai_excel(output_dir, output_file_name="hyundai_demand.xlsx"):
    # ChromeDriver 설정
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": output_dir,  # 다운로드 경로 설정
        "download.prompt_for_download": False,    # 다운로드 확인창 비활성화
        "download.directory_upgrade": True
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    try:
        # 현대자동차 판매 데이터 페이지 열기
        driver.get('https://www.hyundai.com/worldwide/ko/company/ir/ir-resources/sales-results')
        time.sleep(3)  # 페이지 로드 대기

        # 쿠키 배너나 방해 요소 숨기기
        driver.execute_script("""
            var elements = document.querySelectorAll('.ot-sdk-row, .ot-sdk-container');
            elements.forEach(function(element) {
                element.style.display = 'none';
            });
        """)
        time.sleep(1)  # 요소가 숨겨지길 기다림

        # 다운로드 버튼 찾기 및 클릭
        download_button = driver.find_element(By.CSS_SELECTOR, '#salesPerformanceData > div:nth-child(1) > button > i')
        download_button.click()
        time.sleep(5)

        downloaded_files = os.listdir(output_dir)
        for file_name in downloaded_files:
            if file_name.endswith(".xlsx"):
                source = os.path.join(output_dir, file_name)
                destination = os.path.join(output_dir, output_file_name)

                if os.path.exists(destination):
                    os.remove(destination)  # 기존 파일 삭제

                os.rename(source, destination)
                print(f"File renamed and saved as: {output_file_name}")
                break
        else:
            print("No downloaded .xlsx file found to rename.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.close()
        driver.quit()

# 다운로드 경로 설정
output_directory = r"C:\car_system\view\data\raw"
os.makedirs(output_directory, exist_ok=True)  # 폴더가 없으면 생성

# 함수 실행
download_hyundai_excel(output_directory)

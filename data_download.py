from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# 다운로드 경로 설정
download_dir = "C:\\KIMUJUNG\\team_project1\\data"
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # 다운로드 경로 지정
    "download.prompt_for_download": False,      # 다운로드 창 비활성화
    "safebrowsing.enabled": True                # 안전 브라우징 활성화
})

# WebDriver 초기화
driver = webdriver.Chrome(options=chrome_options)


# 웹페이지 접속
url = "https://stat.molit.go.kr/portal/cate/statMetaView.do?hRsId=58"
driver.get(url)

year_list = ['2020','2021','2022','2023','2024']

for year in year_list:
    # 다운로드 버튼 대기
    download_button1 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//a[@onclick="javascript:downFile(\''+year+'년 11월 자동차 등록자료 통계.xlsx\',\''+year+'년 11월 자동차 등록자료 통계.xlsx\',\'/stat_file/\',\'IfrFile\');return false;"]'))
    )

    # JavaScript로 클릭 실행
    driver.execute_script("arguments[0].click();", download_button1)
    time.sleep(5)
driver.quit()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time
import pandas as pd



driver = webdriver.Chrome()

driver.get('https://auto.danawa.com/newcar/?Work=record')
time.sleep(1)

# 기업 선택 경로와 기업명 리스트
xpath_list = ['1','2','4','5','6']
brand_list = ['현대','기아','쉐보레','KGM','르노코리아']
# 저장용 데이터 프레임 생성
car_sales_data = pd.DataFrame({
    "car_brand" : [],
    "sale_year" : [],
    "sale_month" : [],
    "car_name" : [],
    "fuel" : [],
    "car_count" : [],
    "car_total" : []
})
for i in range(len(xpath_list)):
    # 브랜드 선택
    car_btn_elems1 = driver.find_element(By.XPATH, '//*[@id="finder_newcar"]/div[1]/div[1]/div[1]/ul/li['+ xpath_list[i] +']/button/img')
    car_btn_elems1.click()
    car_brand = brand_list[i]
    time.sleep(1)
    
    for j in range(2):
        # 년도 선택
        car_btn_elems2 = driver.find_element(By.XPATH, '//*[@id="selMonth"]/option['+ str(3 - j) +']')
        # option[3] = 2023년, option[2] = 2024년
        car_btn_elems2.click()
        time.sleep(1)

        for k in range(12):
            # 월 선택
            car_btn_elems3 = driver.find_element(By.XPATH, '//*[@id="selDay"]/option['+ str(k + 1) +']')
            # option[1]~[12] : 1월 ~ 12월
            car_btn_elems3.click()
            time.sleep(1)

            # rank를 통해 자동차별 경로 설정
            car_sales_elems = driver.find_element(By.XPATH, '//*[@id="autodanawa_gridC"]/div[3]/article/main/div/table[2]/tbody')
            car_sales_elems2 = car_sales_elems.find_elements(By.CSS_SELECTOR,"tr > td.rank")
            
            for car_sales_elem2 in car_sales_elems2:
                # rank의 형제 선택자 자동차명과 판매량
                car_name = car_sales_elem2.find_element(By.XPATH,'./following-sibling::td[@class = "title"]').text
                car_sales = car_sales_elem2.find_element(By.XPATH,'./following-sibling::td[@class = "num"]').text

                car_sales_elem3 = car_sales_elem2.find_element(By.XPATH, '..')
                # car_sales_elem4 = car_sales_elem3.find_element(By.XPATH, './following-sibling::tr[1]')

                try: # 24년 12월 같이 car_sales_elem4가 없는 경우를 위해 try 사용
                    if len(car_sales_elem3.find_element(By.XPATH, './following-sibling::tr[1]').get_attribute('class')) != 0:
                        car_sales_elem5 = car_sales_elem3.find_element(By.XPATH, './following::td[@class = "total_cont"]')
                        
                        span_elements = car_sales_elem5.find_elements(By.CSS_SELECTOR, 'span')
                        for span in span_elements:
                            span_text = span.get_attribute("textContent").strip()
                            data_tmp = pd.DataFrame({
                                "car_brand" : [car_brand],
                                "sale_year" : [2023 + j],
                                "sale_month" : [1 + k],
                                "car_name" : [car_name],
                                "fuel" : [span_text.split()[0]],
                                "car_count" : [span_text.split()[1]],
                                "car_total" : [car_sales]
                            })
                            car_sales_data = pd.concat([car_sales_data,data_tmp])
                    else:
                        data_tmp = pd.DataFrame({
                            "car_brand" : [car_brand],
                            "sale_year" : [2023 + j],
                            "sale_month" : [1 + k],
                            "car_name" : [car_name],
                            "fuel" : [None],
                            "car_count" : [None],
                            "car_total" : [car_sales]
                        })
                        car_sales_data = pd.concat([car_sales_data,data_tmp])

                    # car_sales_data.to_csv('car_sales_data_' + str(i)+'_' + str(2023 +j)+'_' + str(1+k) +'.csv', index=False)
                except :
                    data_tmp = pd.DataFrame({
                        "car_brand" : [car_brand],
                        "sale_year" : [2023 + j],
                        "sale_month" : [1 + k],
                        "car_name" : [car_name],
                        "fuel" : [None],
                        "car_count" : [None],
                        "car_total" : [car_sales]
                    })
    car_sales_data = pd.concat([car_sales_data, data_tmp])

    # 브랜드 선택 초기화
    car_btn_elems1 = driver.find_element(By.XPATH, '//*[@id="finder_newcar"]/div[1]/div[1]/div[1]/ul/li['+ xpath_list[i] +']/button/img')
    car_btn_elems1.click()
    time.sleep(1)

car_sales_data['sale_month'] = car_sales_data['sale_month'].apply(lambda x : '.0'+str(int(x)) 
                                          if x <10 else  '.' +str(int(x)))

car_sales_data['sale_year'] = car_sales_data['sale_year'].apply(lambda x: str(int(x)))
car_sales_data['sale_month'] = car_sales_data['sale_year'].map(str) + car_sales_data['sale_month'].map(str)

car_sales_data = car_sales_data.drop('car_total',axis=1)
car_sales_data = car_sales_data.drop('sale_year',axis=1)
car_sales_data.rename(columns={'car_brand' : 'brand'},inplace=True)
car_sales_data.rename(columns={'car_name' : 'model_name'},inplace=True)
car_sales_data.rename(columns={'fuel' : 'fuel_name'},inplace=True)
car_sales_data.rename(columns={'car_count' : 'sale_count'},inplace=True)
car_sales_data.dropna(subset=['fuel_name'])

car_sales_data.to_csv('car_sales_data.csv', index=False)
# 가져올 데이터: 자동차 title, 자동차 num(총판매량), sub total -> total_cont(연료별 판매량)
driver.quit()
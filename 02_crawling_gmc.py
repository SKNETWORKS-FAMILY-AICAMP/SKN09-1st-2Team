from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time
import pandas as pd

driver = webdriver.Chrome()

driver.get('https://www.gmckorea.co.kr/faq')
time.sleep(1)

gm_faq_elems = driver.find_elements(By.CSS_SELECTOR, "div.col-con > div.q-mod > div.none-margin")
# print(len(gm_faq_elems))

category_list = []
title_list = []
content_list = []
for gm_faq_elem in gm_faq_elems:
    gm_faq_heads_elem = gm_faq_elem.find_element(By.TAG_NAME, "h3")
    gm_faq_contents_elem = gm_faq_elem.find_element(By.CSS_SELECTOR, ".q-text")

    # print(gm_faq_heads_elem.text)
    # print(gm_faq_contents_elem.text)
    category_list.append(gm_faq_heads_elem.text.split(']')[0]+']')
    title_list.append(gm_faq_heads_elem.text)
    content_list.append(gm_faq_contents_elem.text)


# 파일에 저장
faq_text = pd.DataFrame({
    'brand' : 'GMC',
    'category' : category_list,
    'question' : title_list,
    'answer' : content_list
})
faq_text.to_csv('gmc_faq_data.csv', index=False, encoding='utf-8')

driver.quit()
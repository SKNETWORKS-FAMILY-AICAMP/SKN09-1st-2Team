from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time
import pandas as pd



driver = webdriver.Chrome()

driver.get('https://www.chevrolet.co.kr/faq')
time.sleep(2)

faq_categorys = driver.find_elements(By.CSS_SELECTOR, '#gb-main-content > adv-grid.hide-for-small.hide-for-medium.hide-for-large.none-margin.grid-sm-fw > adv-col.col-sm-12.col-sm-bw-up-2.col-sm-gut-no.col-sm-bs-up-solid.q-cc-ag-lightgray-border > div > adv-grid > adv-col')
print(len(faq_categorys))
for faq_category in faq_categorys:
    category_btn = faq_category.find_element(By.CSS_SELECTOR, 'div > a.q-mod')
    href = category_btn.get_attribute('href')
    category = category_btn.get_attribute('title')
    print(category)
 
    driver.execute_script("window.open('');") # 자바스크립트 실행(새 탭으로 실행)
    driver.switch_to.window(driver.window_handles[1]) # 다른 탭으로 변경
    driver.get(href)
    time.sleep(1)
    title_list = []
    content_list = []
    category_list = []
    faq_elems = driver.find_elements(By.CSS_SELECTOR, 'adv-col.col-sm-12 > div.col-con > div.q-mod')
    print(len(faq_elems))#gb-main-content > gb-adv-grid.gb-small-margin > adv-col > div > div:nth-child(1) > div > div.q-headline.q-expander-button.stat-expand-icon > h3
    for faq_elem in faq_elems:#gb-main-content > adv-grid.large-margin > adv-col > div > div:nth-child(2) > div > div.q-headline.q-expander-button.stat-expand-icon > h6
        faq_heads_elem1 = faq_elem.find_element(By.CSS_SELECTOR, "div > div.q-headline.q-expander-button.stat-expand-icon")
        # print(faq_heads_elem1.get_attribute('data-dtm'))
        faq_heads_elem = faq_heads_elem1.find_element(By.CLASS_NAME, 'q-button-text.q-headline-text')
        faq_contents_elem = faq_elem.find_element(By.CSS_SELECTOR, "div.none-margin > div.q-text")

        # print(faq_heads_elem.text)
        # print(faq_contents_elem.get_attribute("innerText"))
        category_list.append(category)
        title_list.append(faq_heads_elem.text)
        content_list.append(faq_contents_elem.get_attribute("innerText"))

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)


    # 파일에 저장
    faq_text = pd.DataFrame({
        'brand' : 'chevrloet',
        'category' : category,
        'question' : title_list,
        'answer' : content_list
    })
faq_text.to_csv('chevrolet_faq_data.csv', index=False, encoding='utf-8')

driver.quit()
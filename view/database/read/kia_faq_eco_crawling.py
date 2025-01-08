# import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json

# 데이터 저장
kia_electric_vehicle = []

# 크롬 실행
driver = webdriver.Chrome()

# 주소 연결
driver.get("https://www.kia.com/kr/vehicles/kia-ev/guide/faq")
time.sleep(3)  # 대기 시간이 있어야 나옴

# 특정 데이터에 연결
faq_datas = driver.find_elements(By.CSS_SELECTOR, ".cmp-accordion__item")
faq_buttons = driver.find_elements(By.CSS_SELECTOR, ".cmp-accordion__icon")
print(len(faq_datas))

offset = 62

for i, faq_data in enumerate(faq_datas):
    question = faq_data.find_element(By.CSS_SELECTOR, ".cmp-accordion__title").text
    print(question)

    faq_buttons[i].click()
    time.sleep(1)

    answer_elements = faq_data.find_elements(By.CSS_SELECTOR, ".faqinner__wrap p")
    answer_texts = [answer.text for answer in answer_elements]

    # 텍스트들을 ','로 연결하여 출력
    print('\n '.join(answer_texts))

    kia_electric_vehicle.append({
        "id": i + offset,
        "brand": "kia",
        "category": "전기차",
        "question": question,
        "answer": ' '.join(answer_texts)
    })

driver.close()

with open("../../data/raw/kia_ev.json", "w", encoding="utf-8") as file:
    json.dump(kia_electric_vehicle, file, ensure_ascii=False, indent=4)

# with open("kia_electric_vehicle.json", "w", encoding="utf-8") as file:
#        for faq in kia_electric_vehicle:
#         file.write(f"id: {faq['id']}\n")
#         file.write(f"brand: {faq['brand']}\n")
#         file.write(f"category: {faq['category']}\n")
#         file.write(f"question: {faq['question']}\n")  # 여기에서 'faq'를 사용
#         file.write(f"answer: {faq['answer']}\n")

driver.quit()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json

# 1. chrome 실행
driver = webdriver.Chrome()

kia_car = []


# 2. 특정 url 접근
# https://www.kia.com/kr/customer-service/center/faq
def go_faq_main(wait):
    driver.get("https://www.kia.com/kr/customer-service/center/faq")
    time.sleep(wait)


go_faq_main(3)

# 3. 클릭으로 이동하기
top_buttons = driver.find_elements(By.CSS_SELECTOR, ".tabs__btn")
top_buttons_name = ["TOP 10", "전체", "차량 구매", "차량 정비", "기아멤버스", "홈페이지", "PBV", "기타"]
# print(len(top_buttons))
id = 0

for button in top_buttons:
    # go_faq_main(3)

    button.click()
    time.sleep(5)

    faq_section = driver.find_element(By.CSS_SELECTOR, ".cmp-accor-faq.cmp-content__section")
    faq_datas = faq_section.find_elements(By.CSS_SELECTOR, ".cmp-accordion__item")
    faq_buttons = faq_section.find_elements(By.CSS_SELECTOR, ".cmp-accordion__icon")
    category = button.text
    print(len(faq_datas))
    time.sleep(1)

    for j, faq_data in enumerate(faq_datas):
        question = faq_data.find_element(By.CSS_SELECTOR, ".cmp-accordion__title").text
        print(question)

        faq_buttons[j].click()
        time.sleep(1)

        answer_elements = faq_data.find_elements(By.CSS_SELECTOR, ".faqinner__wrap p")
        answer_texts = [answer.text for answer in answer_elements]

        id += 1

        kia_car.append(
            {
                "id": id,
                "brand": "kia",
                "category": category,
                "question": question,
                "answer": ' '.join(answer_texts)
            }
        )

driver.close()

with open("../../data/raw/kia_car.json", "w", encoding="utf-8") as file:
    json.dump(kia_car, file, ensure_ascii=False, indent=4)

# with open("kia_car.json", "w", encoding="utf-8") as file:
#     for faq in kia_car:
#         file.write(f"id: {faq["id"]}\n")
#         file.write(f"brand: {faq["category"]}\n")
#         file.write(f"question: {faq["question"]}\n")
#         file.write(f"answer: {faq["answer"]}\n")


driver.quit()
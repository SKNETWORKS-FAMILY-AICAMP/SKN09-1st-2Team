import pandas as pd
import json

# json -> dataframe
with open("../../data/raw/kia_car.json", "r", encoding="utf-8") as file:
    kia_car_json = json.load(file)

with open("../../data/raw/kia_ev.json", "r", encoding="utf-8") as file:
    kia_ev_json = json.load(file)

kia_car_datafram = pd.DataFrame(kia_car_json)
kia_ev_dataframe = pd.DataFrame(kia_ev_json)

kia_faq_dataframe = pd.concat([kia_car_datafram, kia_ev_dataframe], ignore_index=True)

print(kia_faq_dataframe)

for i, row in kia_car_datafram.iterrows():
    print(f"{row['id'], row['brand'], row['category'], row['question'], row['answer']}")

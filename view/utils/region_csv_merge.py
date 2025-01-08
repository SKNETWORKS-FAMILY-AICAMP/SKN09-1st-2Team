import pandas as pd

df_2020 = pd.read_csv('/view/data/raw/2020_data.csv', encoding='utf-8')
df_2021 = pd.read_csv('/view/data/raw/2021_data.csv', encoding='utf-8')
df_2022 = pd.read_csv('/view/data/raw/2022_data.csv', encoding='utf-8')
df_2023 = pd.read_csv('/view/data/raw/2023_data.csv', encoding='utf-8')
df_2024 = pd.read_csv('/view/data/raw/2024_data.csv', encoding='utf-8')

df_2020.drop(['Unnamed: 0'], axis = 1, inplace = True)
df_2021.drop(['Unnamed: 0'], axis = 1, inplace = True)
df_2022.drop(['Unnamed: 0'], axis = 1, inplace = True)
df_2023.drop(['Unnamed: 0'], axis = 1, inplace = True)
df_2024.drop(['Unnamed: 0'], axis = 1, inplace = True)


df_melted = df_2024.melt(id_vars=['연료별'], var_name='region', value_name='region_regist')

df_melted['whole_region_car_regist'] = df_melted[df_melted['region'] == '계']['region_regist'].values[0]

df_melted = df_melted[df_melted['region'] != '계']

df_melted.insert(0, 'regist_date', '2024.11')

df_melted = df_melted.rename(columns={'연료별': 'fuel_type'})

df_melted.to_csv('C:/car_system/view/data/raw/2024_car_regist.csv', encoding='utf-8')

df_2020 = pd.read_csv('/view/data/raw/2020_car_regist.csv', encoding='utf-8')
df_2021 = pd.read_csv('/view/data/raw/2021_car_regist.csv', encoding='utf-8')
df_2022 = pd.read_csv('/view/data/raw/2022_car_regist.csv', encoding='utf-8')
df_2023 = pd.read_csv('/view/data/raw/2023_car_regist.csv', encoding='utf-8')
df_2024 = pd.read_csv('/view/data/raw/2024_car_regist.csv', encoding='utf-8')

df_concat = pd.concat([df_2020, df_2021, df_2022, df_2023, df_2024], axis=0, ignore_index=True)

df_concat.to_csv('C:/car_system/view/data/raw/whole_car_regist.csv', encoding='utf-8')
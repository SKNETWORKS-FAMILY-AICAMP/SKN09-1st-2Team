import pandas as pd
year_list = [str(i) for i in range(2020,2025)]

data_dic = {}
for year in year_list:
    data_1 = pd.read_excel('C:/car_system/view/data/raw/'+ year +'년_11월_자동차_등록자료_통계.xlsx', sheet_name='10.연료별_등록현황',skiprows=2)
    if year in year[0:4]:
        data_1[['연료별','시도별']] = data_1[['연료별','시도별']].fillna(method='ffill')
    data_2 = data_1[(data_1['시도별'] == '소계') & (data_1['Unnamed: 2'] == "계")]
    data_2 = data_2.drop(['시도별','Unnamed: 2'], axis=1)

    # exec(f'data_{year} = data_2')
    data_dic['data_' + year] = data_2

    dd = data_dic['data_'+ year]
    dd.to_csv('C:/car_system/view/data/raw/'+year+'_data.csv', encoding='utf-8')
import pandas as pd

def filter_hev_ev(data: pd.DataFrame, model_column: str = "Unnamed: 2", month_start: str = "Jan.", month_end: str = "Dec."):
    data_fixed = data.drop(columns=["Unnamed: 0", "Unnamed: 1"], errors="ignore")
    filtered_data = data_fixed[data_fixed[model_column].str.contains("HEV|EV", na=False, case=False)]
    model_list = filtered_data[model_column].tolist()

    monthly_data = filtered_data.loc[:, month_start:month_end].apply(pd.to_numeric, errors='coerce')
    monthly_data.index = filtered_data[model_column]

    return model_list, monthly_data
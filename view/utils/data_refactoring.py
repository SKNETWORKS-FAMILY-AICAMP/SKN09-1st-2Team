from view.database.read.hyundai_faq_page_read import load_data_from_database
import pandas as pd

def make_dataframe():
    data = load_data_from_database()
    df = pd.DataFrame(data, columns=['id', 'brand', 'category', 'question', 'answer'])
    df['question'] = df['question'].str.replace(r"\[.*?\]\\n", "", regex=True)
    df['question'] = df['question'].str.replace(r"\\n", " ", regex=True)
    df['answer'] = df['answer'].str.replace(r"\\n", "\n", regex=True)

    return df

def filter_hev_ev(data: pd.DataFrame, model_column: str = "Unnamed: 2", month_start: str = "Jan.", month_end: str = "Dec."):
    data_fixed = data.drop(columns=["Unnamed: 0", "Unnamed: 1"], errors="ignore")
    filtered_data = data_fixed[data_fixed[model_column].str.contains("HEV|EV", na=False, case=False)]
    model_list = filtered_data[model_column].tolist()

    monthly_data = filtered_data.loc[:, month_start:month_end].apply(pd.to_numeric, errors='coerce')
    monthly_data.index = filtered_data[model_column]

    return model_list, monthly_data

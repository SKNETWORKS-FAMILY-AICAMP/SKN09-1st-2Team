from view.utils.file_loader import load_excel
from view.utils.data_cleaning import filter_hev_ev

def process_hundae_data(sheet_name="Unit Sales by Model"):
    try:
        # 현대 자동차 데이터 로드
        data = load_excel(sheet_name=sheet_name, file_name="hundae.xlsx", header=2)
        # 데이터 필터링
        model_list, monthly_sales = filter_hev_ev(data, model_column="Unnamed: 2", month_start="Jan.", month_end="Dec.")
        return model_list, monthly_sales
    except FileNotFoundError:
        return [], None
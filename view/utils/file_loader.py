import os
import pandas as pd

def load_excel(sheet_name: str, file_name: str = "hyundai_demand.xlsx", header: int = 2):

    base_path = os.path.dirname(os.path.abspath(__file__))
    view_path = os.path.dirname(base_path)
    file_path = os.path.join(view_path, "data", "raw", file_name)

    try:
        data = pd.read_excel(file_path, sheet_name=sheet_name, header=header)
        print(data)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_name}' was not found in '{file_path}'")

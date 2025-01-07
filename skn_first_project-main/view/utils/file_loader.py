import os
import pandas as pd

def load_excel(sheet_name: str, file_name: str = "hundae.xlsx", header: int = 2):

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    file_path = os.path.join(project_root, "data", "raw", file_name)

    try:
        data = pd.read_excel(file_path, sheet_name=sheet_name, header=header)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_name}' was not found in '{file_path}'")
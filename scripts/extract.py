import pandas as pd
import os

RAW_EXCEL_PATH = "data/raw/excel"
RAW_SQL_PATH = "data/raw/sqlserver"
PROCESSED_PATH = "data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)

def extract_excel():
    excel_data = {}
    for file in os.listdir(RAW_EXCEL_PATH):
        if file.endswith(".xlsx"):
            name = file.replace(".xlsx", "")
            path = os.path.join(RAW_EXCEL_PATH, file)
            excel_data[name] = pd.read_excel(path)
            print(f"✔ Excel chargé : {file}")
    return excel_data

def extract_sql_csv():
    sql_data = {}
    for file in os.listdir(RAW_SQL_PATH):
        if file.endswith(".csv"):
            name = file.replace(".csv", "")
            path = os.path.join(RAW_SQL_PATH, file)
            sql_data[name] = pd.read_csv(path)
            print(f"✔ CSV SQL chargé : {file}")
    return sql_data

if __name__ == "__main__":
    excel_data = extract_excel()
    sql_data = extract_sql_csv()

    for name, df in {**excel_data, **sql_data}.items():
        df.to_csv(f"{PROCESSED_PATH}/{name}.csv", index=False)

    print("✅ Extraction terminée")

import os.path
from datetime import datetime

import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="nuttygritties"
)

current_date = datetime.now().strftime("%d_%m_%Y")  # 2024/08/0

# sql_query = "select * from product_data;"
sql_query = f"select * from product_data_{current_date};"

df = pd.read_sql(sql_query, mydb)

current_date = datetime.now().strftime("%d_%m_%Y")  # 2024/08/0

excel_file_path = f'D:\\Nirav_live_project_export_data\\nuttygritties'
if not os.path.exists(excel_file_path):
    os.makedirs(excel_file_path)
    excel_file_path = excel_file_path + f"\\nuttygritties_{current_date}.xlsx"
    df.to_excel(excel_file_path, index=False)
else:
    excel_file_path = excel_file_path + f"\\nuttygritties_{current_date}.xlsx"
    df.to_excel(excel_file_path, index=False)

print("Your excel file generated..")

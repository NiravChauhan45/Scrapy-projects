import os.path
from datetime import datetime

import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="chatime_canada"
)

current_date = datetime.now().strftime("%d_%m_%Y")  # 2024/08/0

# sql_query = "select * from product_data;"
sql_query = f"select * from locations_data"

df = pd.read_sql(sql_query, mydb)

current_date = datetime.now().strftime("%d_%m_%Y")  # 2024/08/0

excel_file_path = f'F:\\Nirav_live_project_export_data\\chatime_canada'
if not os.path.exists(excel_file_path):
    os.makedirs(excel_file_path)
    excel_file_path = excel_file_path + f"\\chatime_canada_{current_date}.xlsx"
    df.to_excel(excel_file_path, index=False)
else:
    excel_file_path = excel_file_path + f"\\chatime_canada_{current_date}.xlsx"
    df.to_excel(excel_file_path, index=False)

print("Your excel file generated..")

import os.path
from datetime import datetime

import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="kawasaki_usa"
)

current_date = datetime.now().strftime("%d_%m_%Y")  # 2024/08/0

# sql_query = "select * from product_data;"
sql_query = f"select * from kawasaki_locations_data"

df = pd.read_sql(sql_query, mydb)

excel_file_path = f'F:\\Nirav\\Project_export_data\\kawasaki_usa'
if not os.path.exists(excel_file_path):
    os.mkdir(excel_file_path)
    excel_file_path = excel_file_path + f"\\kawasaki_usa_{current_date}.xlsx"
    df.to_excel(excel_file_path, index=False)
else:
    excel_file_path = excel_file_path + f"\\kawasaki_usa_{current_date}.xlsx"
    df.to_excel(excel_file_path, index=False)

print("Your excel file generated..")

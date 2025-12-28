import os.path
from datetime import datetime

import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="kohinoor_electronics"
)

today_date = datetime.now().strftime("%d_%m_%Y")

sql_query = "select * from product_data;"
df = pd.read_sql(sql_query, conn)
excel_path = "F:\\Nirav\\Project_export_data\\kohinoor_electronics\\"

if not os.path.exists(excel_path):
    os.mkdir(excel_path)

excel_path = excel_path + f"kohinoor_electronics_{today_date}.xlsx"

drop_extra_columns = df.drop(labels='id', axis=1)

drop_extra_columns.to_excel(excel_path, index=False)
print(f"Your excel file has been generated, total count is: {df['id'].count()}")

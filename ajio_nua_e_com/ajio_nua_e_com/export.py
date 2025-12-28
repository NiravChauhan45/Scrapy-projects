import os.path
from datetime import datetime

import numpy as np
import pandas as pd
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="ajio_nua_ecomm"
)

today_date = datetime.now().strftime("%d_%m_%Y")

# sql_query = "select * from pdp_data;"
sql_query = f"select * from pl_data_{today_date};"
df = pd.read_sql(sql_query, conn)
excel_path = f"D:\\Nirav Chauhan\\Data\\ajio_nua_ecomm\\{today_date}"
os.makedirs(excel_path, exist_ok=True)
excel_path = f"{excel_path}\\ajio_nua_ecomm_{today_date}.xlsx"
df = df.replace('', np.nan).fillna("N/A")
del df['unique_key']
df.to_excel(excel_path, index=False, engine="openpyxl")

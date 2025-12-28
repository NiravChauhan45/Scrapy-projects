import nykaa_saller.db_config as db
from datetime import datetime
import pandas as pd
import pymysql
import os

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database=db.database_name
)
sql_query = f"select * from pdp_data_{db.current_date};"
df = pd.read_sql(sql_query, conn)

df = df.drop_duplicates()
filepath = f"E:\\Nirav\\Project_export_data\\{db.database_name}\\{db.current_date}"
os.makedirs(filepath, exist_ok=True)
excel_filepath = f"{filepath}\\{db.database_name}_{db.current_date}.xlsx"
csv_filepath = f"{filepath}\\{db.database_name}_{db.current_date}.csv"
# df['shipping_charges'] = df['shipping_charges'].apply(
#     lambda x: "N/A" if pd.notnull(x) and str(x).isdigit() and int(x) == 0 else x
# )
df.fillna("N/A", inplace=True)
df = df.replace('0', "N/A")
df = df.replace('', "N/A")
df = df.replace(0.0, "N/A")
df = df.replace(0, "N/A")
df.to_excel(excel_filepath, index=False)
df.to_csv(csv_filepath, index=False, encoding='utf-8-sig', sep=';')

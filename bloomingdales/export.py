import db_config as db
import pandas as pd
import pymysql
import os

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database=db.database_name
)

sql_query = (
    f"select * from pdp_data_{db.current_date} "
    f"where Category REGEXP '(Fashion|Footwear|Shoes|Accessories|Beauty|Men|Women)';"
)
df = pd.read_sql(sql_query, conn)


def modify_data(row):
    print(row['Name'])


df = df.drop_duplicates()

filepath = f"D:\\Nirav Chauhan\\Data\\{db.database_name}\\{db.current_date}"
os.makedirs(filepath, exist_ok=True)

excel_filepath = f"{filepath}\\{db.database_name}_{db.current_date}.xlsx"

df.fillna("N/A", inplace=True)

df['Discount'] = df['Discount'].apply(
    lambda x: "N/A"
    if (pd.notnull(x) and str(x).isdigit() and int(x) == 0) or x == '0'
    else x
)

df = df.replace(0.0, "N/A")
df = df.replace("Write the first review", "N/A")

df['S.No.'] = range(1, len(df) + 1)

# df = df.apply(modify_data, axis=1)

with pd.ExcelWriter(
        excel_filepath,
        engine="xlsxwriter",
        engine_kwargs={"options": {"strings_to_urls": False}}
) as writer:
    df.to_excel(writer, index=False)

import hashlib
from datetime import datetime

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

sql_query = f"select * from pdp_data_{db.current_date}"
df = pd.read_sql(sql_query, conn)


def client_updates(row):
    if not row['SKU']:
        row['SKU'] = row['PID']
    if row['Price'] == "N/A":
        row['Price Currency'] = "N/A"
    row['PID'] = row['PID']
    row['hash_id'] = hashlib.sha256(str(row['PID']).encode()).hexdigest()[:12]
    mpn = str(row['PID']) + str(row['Colour'])
    row['MPN'] = hashlib.sha256(mpn.encode()).hexdigest()[:12]
    if not row['Alternate Image URLs']:
        row['Alternate Image URLs'] = "N/A"
    return row


# Todo: If x is zero → return N/A
def clean_discount(x):
    if (pd.notnull(x) and str(x).isdigit() and int(x) == 0) or x == '0':
        return "N/A"

    # Todo: Try converting to float
    try:
        return round(float(x), 2)
    except (ValueError, TypeError):
        return "N/A"


df = df.drop_duplicates()

filepath = f"D:\\Nirav Chauhan\\Data\\{db.database_name}\\{db.current_date}"
os.makedirs(filepath, exist_ok=True)
current_date = datetime.now().strftime("%Y%m%d")
excel_filepath = f"{filepath}\\{db.database_name}_{current_date}.xlsx"

# TODO: Round the "Discount" column to 2 decimal places & Also Handling Nulls values
df['Discount'] = df['Discount'].apply(clean_discount)

# Todo: NULL's Values Handlings
df.fillna("N/A", inplace=True)
df = df.replace(0.0, "N/A")
df = df.replace("Write the first review", "N/A")

df = df.apply(client_updates, axis=1)

# Todo: Set S.No. column in sequence
df['S.No.'] = range(1, len(df) + 1)

# Todo: To change datatype integer to string
df["Price"] = df["Price"].astype(str)
df["Sale Price"] = df["Sale Price"].astype(str)
df["Final Price"] = df["Final Price"].astype(str)
df["Discount"] = df["Discount"].astype(str)
df["MPN"] = df["MPN"].astype(str)
df["Varint_Price"] = df["Varint_Price"].astype(str)
df["Num Ratings"] = df["Num Ratings"].astype(str)
df["Average Ratings"] = df["Average Ratings"].astype(str)
df["hash_id"] = df["hash_id"].astype(str)
df["pagesave_id"] = df["pagesave_id"].astype(str)

# Todo: To Convert Lowercase To Uppercase
df['IsInStock'] = df['IsInStock'].str.upper()

with pd.ExcelWriter(
        excel_filepath,
        engine="xlsxwriter",
        engine_kwargs={"options": {"strings_to_urls": False}}
) as writer:
    df.to_excel(writer, index=False)

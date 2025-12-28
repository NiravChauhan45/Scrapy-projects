import os

import pandas as pd

from datetime import datetime
import numpy as np

today_date = datetime.now().strftime("%d_%m_%Y")
excel_path = f"F:\\Nirav\\Project_export_data\\Amazon\\"
os.makedirs(excel_path, exist_ok=True)
excel_path = excel_path + f"Amazon_Namkeen_{today_date}.xlsx"

df1 = pd.read_excel(
    f"F:\\Nirav\\Project_export_data\\Amazon\\Amazon_namkeen_21_02_2025_old.xlsx")

df1['Product_Name'] = df1['Product_Name'].str.encode('ascii', 'ignore').str.decode('ascii')
df1['Mrp'] = df1['Mrp'].astype(str).apply(lambda x: x.replace(',', ''))
df1['Price'] = df1['Price'].astype(str).apply(lambda x: x.replace(',', ''))

for column in ['Price', 'Mrp']:
    df1[column] = df1[column].apply(lambda c1: "N/A" if str(c1).lower() == 'nan' else c1)


# B01B26BO9G

def update_stock(row):
    if row['Mrp'] == 'N/A' and row['Price'] == 'N/A':
        return 'OutofStock'
    return row['In_Stock']


df1 = df1.replace('', np.nan).fillna('N/A')
df1.replace(np.NaN, 'N/A', inplace=True)
df1.replace('', 'N/A', inplace=True)
df1.fillna('N/A')
df1['In_Stock'] = df1.apply(update_stock, axis=1)
df1.to_excel(excel_path, index=False, engine="xlsxwriter")
print(f"Your excel file has been generated, total count is: {df1['Product_Id'].count()}")

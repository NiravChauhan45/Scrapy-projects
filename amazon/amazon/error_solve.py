import os
from datetime import datetime

import numpy as np
import pandas as pd


def get_tag(tag):
    if tag:
        aa = str(tag).split(' | ')
        li = list()
        for j in aa:
            li.append(j.strip())
        if li:
            return li


today_date = datetime.now().strftime("%d_%m_%Y")
excel_path = f"F:\\Nirav\\Project_export_data\\Amazon\\"
os.makedirs(excel_path, exist_ok=True)
excel_path = excel_path + f"Amazon_Namkeen_{today_date}.xlsx"

df1 = pd.read_excel(
    f"F:\\Nirav\\Project_export_data\\Amazon\\Amazon_namkeen_21_02_2025.xlsx")
del df1['Id']
df1.columns = df1.columns.str.lower()
df1['in_stock'] = np.where(df1['in_stock'] == "InStock", "TRUE", "FALSE")
df1['tag'] = df1['tag'].apply(get_tag)

df1[['mrp', 'price']] = df1[['mrp', 'price']].fillna(0).astype(int)
df1 = df1.replace('', np.nan).fillna('N/A')
df1.replace(np.NaN, 'N/A', inplace=True)
df1.replace('', 'N/A', inplace=True)
df1.replace(0, 'N/A', inplace=True)
df1.fillna('N/A')
df1.to_excel(excel_path, index=False, engine="xlsxwriter")
print(f"Your excel file has been generated, total count is: {df1['product_id'].count()}")

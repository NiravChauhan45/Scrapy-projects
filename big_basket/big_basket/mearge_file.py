from datetime import datetime

import numpy as np
import pandas as pd

# Load the first Excel file
# df1 = pd.read_excel("file1.xlsx")
today_date = datetime.now().strftime("%d_%m_%Y")

# Load the second Excel file
df1 = pd.read_excel(f"F:\\Nirav\\Project_export_data\\big_basket\\{today_date}\\big_basket_{today_date}_namkeen.xlsx")
df2 = pd.read_excel(f"F:\\Nirav\\Project_export_data\\big_basket\\{today_date}\\big_basket_{today_date}_namkin.xlsx")

# Merge the data (concatenation)
merged_df = pd.concat([df1, df2], ignore_index=True)
merged_df['discount'] = merged_df['discount'].round(2)
# Save the merged file
excel_path = f"F:\\Nirav\\Project_export_data\\big_basket\\{today_date}\\"

excel_path = excel_path + f"big_basket_{today_date}.xlsx"
merged_df = merged_df.replace('', np.nan).fillna('N/A')
merged_df.to_excel(excel_path, index=False, engine="xlsxwriter")

print("Excel files merged successfully!")

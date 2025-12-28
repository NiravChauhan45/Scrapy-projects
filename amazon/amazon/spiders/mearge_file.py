from datetime import datetime
import numpy as np
import pandas as pd

today_date = datetime.now().strftime("%d_%m_%Y")
excel_path = f"F:\\Nirav\\Project_code\\amazon\\amazon\\output_files\\"
excel_path = excel_path + f"Amazon_Namkeen_{today_date}.xlsx"

brand_df = pd.read_excel(
    f"F:\\Nirav\\Project_code\\amazon\\amazon\\output_files\\Amazon_namkeen_21_02_2025_brands.xlsx")

discount_df = pd.read_excel(
    f"F:\\Nirav\\Project_code\\amazon\\amazon\\output_files\\Amazon_namkeen_21_02_2025_Discount.xlsx")

seller_1_df = pd.read_excel(
    f"F:\\Nirav\\Project_code\\amazon\\amazon\\output_files\\Amazon_namkeen_21_02_2025_seller_1.xlsx")

seller_2_to_6_df = pd.read_excel(
    f"F:\\Nirav\\Project_code\\amazon\\amazon\\output_files\\Amazon_namkeen_21_02_2025_seller_2_to_6.xlsx")

speciality_df = pd.read_excel(
    "F:\\Nirav\\Project_code\\amazon\\amazon\\output_files\\Amazon_namkeen_21_02_2025_specialty.xlsx")

merged_df = pd.concat([brand_df, discount_df, seller_1_df, seller_2_to_6_df, speciality_df], ignore_index=True)
merged_df = merged_df.replace('', np.nan).fillna('N/A')
merged_df.replace(np.NaN, 'NA', inplace=True)
merged_df.replace('', 'NA', inplace=True)
merged_df = merged_df.drop_duplicates()
merged_df.to_excel(excel_path, index=False, engine="xlsxwriter")

print("Excel files merged successfully!")

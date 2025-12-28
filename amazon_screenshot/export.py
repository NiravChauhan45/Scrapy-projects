import os.path
import re
import db_config as db
import numpy as np
import pandas as pd
import pymysql

from loguru import logger

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database=db.database_name
)


def get_quantity_caping(quantity_caping):
    if quantity_caping == 0 or quantity_caping == '0':
        return "N/A"
    else:
        return quantity_caping


def remove_junck_characters(text):
    text = re.sub(r'[^a-zA-Z0-9\s.,&\'’-]', '',
                  text)  # Keep only alphanumeric characters, punctuation, and necessary symbols
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    cleaned_text = re.sub(r'&amp;', '&', text)
    cleaned_text = re.sub(r'&amp', '&', cleaned_text)
    return cleaned_text


os.makedirs(db.data_filepath, exist_ok=True)

sql_query = f"select * from {db.pdp_data_table};"
df = pd.read_sql(sql_query, conn)
# df['Description'] = df['Description'].apply(remove_junck_characters)
df = df.fillna("N/A")
df = df.replace('', np.nan).fillna("N/A")
df = df.replace('[]', np.nan).fillna("N/A")
df = df.replace("None", np.nan).fillna("N/A")

# # Todo: uncomment below code if we need to remove some specific sub_category/category
# excluded_categories = ['Tops & Tunics', 'Dupattas', 'Kaftans', 'Jumpsuits', 'Sherwani', 'Sleepwear', 'N/A']
# filtered_df = df[~df['Sub Category'].isin(excluded_categories)]
df.drop(columns=['hash_id', 'Remarks', 'Packaging of the product'], inplace=True)

df = df[[
    "Sr.No", "Portal Name", "Time (Crawler Time)", "Date (Crawler Date)", "City Name", "Pincode",
    "Brand",
    "Category", "SKU Name", "Pack Size", "Single Pack", "Bundle Pack", "Per Gm Price (Unit Price)", "MRP",
    "Selling price", "Discount (%)", "Save Rs.", "Quantity", "On-site SKU Name", "Availability Status",
    "Quantity Caping", "Product Url", "SKU Packshot", "amazon_approve_not_approve"
]]
df.rename(columns={'amazon_approve_not_approve': 'Amazon Fresh --  Approved/ Not Approved'}, inplace=True)

# filename = fr"{db.data_filepath}\{db.amazon_filename}.xlsx"
filename = fr"{db.data_filepath}\{db.amazon_filename}.xlsx"
df['Quantity Caping'] = df['Quantity Caping'].apply(get_quantity_caping)
df.to_excel(filename, index=False, engine="xlsxwriter")

logger.success(f"Your excel file has been generated, total count is: {df['Sr.No'].count()}")

# Todo: drive link :- https://drive.google.com/drive/folders/1T1lUe10FQLxultRfygiIo85F3WAOUVF0

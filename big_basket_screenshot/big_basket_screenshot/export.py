import os.path
import re
from datetime import datetime

from sqlalchemy import column

import db_config as db
import numpy as np
import pandas as pd
import pymysql
import mysql.connector

from loguru import logger

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="big_basket_screenshot"
)


def remove_extra_space(text):
    if pd.isna(text):
        return 'N/A'
    text = str(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def per_price_unit(text):
    if "rs" in text.lower():
        pattern = r'(\d+(\.\d+)?)/(kg|k|l)'
        matches = re.findall(pattern, text)

        # Extract just the full match (number + unit)
        results = [match[0] + '/' + match[2] for match in matches]
        return "".join(results)
    else:
        return text


def get_price(text):
    if "rs" in text.lower():
        pattern = r'Rs\s*(\d+(\.\d+)?)'
        match = re.search(pattern, text)
        if match:
            price = match.group(1)
            return price
    else:
        return text


def get_filetr_data(row):
    if row['Availability Status'] == 'Not listed' or row['Availability Status'] == 'Out of Stock':
        row['Quantity Caping'] = "N/A"
    return row


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
df = df.fillna("N/A")
df = df.replace('', np.nan).fillna("N/A")
df = df.replace('[]', np.nan).fillna("N/A")
df = df.replace("None", np.nan).fillna("N/A")

# Todo: uncomment below code if we need to remove some specific sub_category/category

df.drop(columns=['hash_id', 'Remarks', 'Packaging of the product'], inplace=True)

df = df[[
    "Sr.No", "Portal Name", "Time (Crawler Time)", "Date (Crawler Date)", "City Name", "Pincode",
    "Brand",
    "Category", "SKU Name", "Pack Size", "Single Pack", "Bundle Pack", "Per Gm Price (Unit Price)", "MRP",
    "Selling price", "Discount (%)", "Save Rs.", "Quantity", "On-site SKU Name", "Availability Status",
    "Quantity Caping", "Product Url", "SKU Packshot", "big_basket_approve_not_approve",
]]

filename = fr"{db.data_filepath}\{db.big_basket_filename}.xlsx"
df['On-site SKU Name'] = df['On-site SKU Name'].apply(remove_extra_space)
df['Per Gm Price (Unit Price)'] = df['Per Gm Price (Unit Price)'].apply(per_price_unit)
df['Selling price'] = df['Selling price'].apply(get_price)
df['MRP'] = df['MRP'].apply(get_price)
df.rename(columns={'big_basket_approve_not_approve': 'BigBasket --  Approved/ Not Approved'}, inplace=True)
df = df.apply(get_filetr_data, axis=1)
df.to_excel(filename, index=False, engine="xlsxwriter")

logger.success(f"Your excel file has been generated, total count is: {df['Sr.No'].count()}")

# Todo: drive link :- https://drive.google.com/drive/folders/1T1lUe10FQLxultRfygiIo85F3WAOUVF0

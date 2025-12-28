import os.path
import re
from datetime import datetime
import db_config as db
import numpy as np
import pandas as pd
import mysql.connector

from loguru import logger

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="amazon_fresh_screenshot"
)


def remove_junck_characters(text):
    text = re.sub(r'[^a-zA-Z0-9\s.,&\'’-]', '',
                  text)  # Keep only alphanumeric characters, punctuation, and necessary symbols
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    cleaned_text = re.sub(r'&amp;', '&', text)
    cleaned_text = re.sub(r'&amp', '&', cleaned_text)
    return cleaned_text


os.makedirs(db.filepath, exist_ok=True)

sql_query = f"select * from {db.amazon_pdp_data};"
df = pd.read_sql(sql_query, conn)
# df['Description'] = df['Description'].apply(remove_junck_characters)
df = df.fillna("N/A")
df = df.replace('', np.nan).fillna("N/A")
df = df.replace('[]', np.nan).fillna("N/A")
df = df.replace("None", np.nan).fillna("N/A")

# df.drop(columns=['hash_id'], inplace=True)
df.drop(columns=['hash_id', 'Remarks', 'Packaging of the product'], inplace=True)

# df=df[[]]
df = df[[
    "Sr.No", "Portal Name","Time (Crawler Time)", "Date (Crawler Date)", "City Name", "Pincode",
    "Brand",
    "Category", "SKU Name", "Pack Size", "Single Pack", "Bundle Pack", "Per Gm Price (Unit Price)", "MRP",
    "Selling price", "Discount (%)", "Save Rs.", "Quantity", "On-site SKU Name", "Availability Status",
    "Quantity Caping", "Product Url","SKU Packshot"
]]

filename = fr"{db.filepath}\{db.amazon_filename}"
df.to_excel(f"{filename}.xlsx", index=False, engine="xlsxwriter")

logger.success(f"Your excel file has been generated, total count is: {df['Sr.No'].count()}")

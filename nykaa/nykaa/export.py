import os.path
import re
from datetime import datetime

import numpy as np
import pandas as pd
import mysql.connector
import db_file as db
from loguru import logger

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="nykaa_twice_week"
)


def remove_junck_characters(text):
    text = re.sub(r'[^a-zA-Z0-9\s.,&\'’-]', '',
                  text)  # Keep only alphanumeric characters, punctuation, and necessary symbols
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    cleaned_text = re.sub(r'&amp;', '&', text)
    cleaned_text = re.sub(r'&amp', '&', cleaned_text)
    return cleaned_text


os.makedirs(db.filepath, exist_ok=True)

sql_query = f"select * from {db.pdp_data_table};"
df = pd.read_sql(sql_query, conn)
df['Description'] = df['Description'].apply(remove_junck_characters)
df = df.fillna("N/A")
df = df.replace('', np.nan).fillna("N/A")
df = df.replace('[]', np.nan).fillna("N/A")
df = df.replace("None", np.nan).fillna("N/A")

# # Todo: uncomment below code if we need to remove some specific sub_category/category
excluded_categories = ['Tops & Tunics', 'Dupattas', 'Kaftans', 'Jumpsuits', 'Sherwani','Sleepwear','N/A']
filtered_df = df[~df['Sub Category'].isin(excluded_categories)]
filtered_df.drop(columns=['pagesave_id', 'hash_id'], inplace=True)
filtered_df.to_excel(db.filename, index=False, engine="xlsxwriter")

logger.success(f"Your excel file has been generated, total count is: {filtered_df['Sr.No'].count()}")

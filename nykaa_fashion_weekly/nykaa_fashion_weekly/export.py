import re
from datetime import datetime
import pandas as pd
import pymysql
import os
import db_config as db

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database=db.database_name
)
sql_query = f"select * from pdp_data_{datetime.now().strftime('%d_%m_%Y')};"
df = pd.read_sql(sql_query, conn)

# df = df.drop(columns=['_id'], errors='ignore')

if 'product_id' in df.columns:
    df['product_id'] = df['product_id'].astype(str)


# cleaning functions
def remove_extra_space(text): return re.sub(r"\s+", " ", str(text)).strip()


def remove_duplicate(text): return " | ".join(set(str(text).split(" | ")))


def clean_category(text): return " | ".join(re.sub(r"\s+", " ", t).strip() for t in str(text).split("|"))


def change_date_formate(date_text):
    return str(date_text)

def category_hierarchy(text):
    text = text.replace('Nykaa >','')
    text = text.replace('Home >','')
    return text.strip()

def is_sold_out(text):
    if text == str(0):
        text = "False"
    else:
        text = "True"
    return text

def page_url(text):
    text = "N/A"
    return text

def position(text):
    text = "N/A"
    return text

cleaning_map = {
    "seller_return_policy": [remove_extra_space, remove_duplicate],
    "specifications": [remove_extra_space],
    "product_details": [remove_extra_space],
    "bank_offers": [remove_extra_space],
    "Best_offers": [remove_extra_space],
    "manufacturing_info_manufacturerInfo": [remove_extra_space],
    "category_hierarchy": [clean_category],
}

for col, funcs in cleaning_map.items():
    if col in df.columns:
        for func in funcs:
            df[col] = df[col].apply(func)

df = df.drop_duplicates()

TODAY = datetime.now().strftime("%d_%m_%Y")
filepath = f"E:\\Nirav\\Project_export_data\\Nykaa_Fashion_Weekly\\{TODAY}"
os.makedirs(filepath, exist_ok=True)
filepath = f"{filepath}\\Nykaa_Fashion_{db.input_name}_{TODAY}.xlsx"
df.fillna("N/A", inplace=True)
df['scraped_date'] = df['scraped_date'].apply(change_date_formate)

header_sequence = ["Id", "product_id", "catalog_name", "catalog_id", "source", "scraped_date", "product_name",
                   "image_url", "category_hierarchy", "product_price", "arrival_date", "shipping_charges",
                   "is_sold_out",
                   "discount", "mrp", "page_url", "product_url", "number_of_ratings", "avg_rating", "position",
                   "country_code",
                   "images", "Best_price", "Best_offers", "bank_offers", "product_details", "specifications", "rating",
                   "MOQ",
                   "brand", "product_code", "Available_sizes", "sellerPartnerId", "seller_return_policy",
                   "manufacturing_info_packerInfo",
                   "manufacturing_info_seller_name", "manufacturing_info_importerInfo",
                   "manufacturing_info_countryOfOrigin", "manufacturing_info_manufacturerInfo",
                   "More_colours", "variation_id"
                   ]
df = df[header_sequence]


df['category_hierarchy'] = df['category_hierarchy'].apply(category_hierarchy)
df['is_sold_out'] = df['is_sold_out'].apply(is_sold_out)
df['page_url'] = df['page_url'].apply(page_url)
df['position'] = df['position'].apply(position)
df.to_excel(filepath, index=False)

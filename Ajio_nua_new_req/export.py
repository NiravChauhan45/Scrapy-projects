import re
from datetime import datetime
import pymongo
import pandas as pd
import os

from unicodedata import category

import config

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'Ajio_nua_new_req'

# current_date = datetime.now().strftime("%Y_%m_%d")
processed_collection_name = f'Product_details_{config.TODAY}'
# processed_collection_name = f'Product_details_13_10_2025'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[processed_collection_name]

data = collection.find()
data_list = list(data)


def remove_extra_space_category_heirarchy(text):
    text_list = text.split('|')
    category_hierarchy = []
    if text_list:
        for text in text_list:
            text = re.sub("\\s+", " ", text).strip()
            category_hierarchy.append(text)
        return " | ".join(category_hierarchy)
    else:
        return text


def remove_extra_space(text):
    text = re.sub("\\s+", " ", text).strip()
    return text


df = pd.DataFrame(data_list)
# Drop MongoDB's default _id column
df = df.drop(columns=['_id'], errors='ignore')

# Convert product_id to string if it exists
if 'product_id' in df.columns:
    df['product_id'] = df['product_id'].astype(str)

df.insert(0, 'id', range(1, len(df) + 1))

if os.path.exists(config.EXCEL_FILE):
    os.remove(config.EXCEL_FILE)
    print(f"Existing file '{config.EXCEL_FILE}' removed.")

# df['product_details'] = df['product_details'].apply(remove_extra_space)
# df['category_heirarchy'] = df['category_heirarchy'].apply(remove_extra_space_category_heirarchy)
df['no_of_reviews'] = "N/A"
df['seller_name'] = "N/A"
df = df.drop_duplicates()

fields = matched_fields = [
    "product_id",
    "catalog_name",
    "catalog_id",
    "source",
    "scraped_date",
    "product_name",
    "image_url",
    "product_price",
    "is_sold_out",
    "discount",
    "mrp",
    "product_url",
    "number_of_ratings",
    "avg_rating",
    "no_of_reviews",
    "images",
    "product_details",
    "specifications",
    "seller_name",
    "Brand",
    "product_code"
]

df = df[fields]

df = df.rename(columns={
    "Image_url": "image_url",
    "seller_name": "Seller Name",
    "brand": "Brand",
    "no_of_reviews": "No of reviews"
})

df['Brand'] = df['Brand'].apply(remove_extra_space)

df.insert(0, "Sr.no", range(1, len(df) + 1))
df.to_excel(config.EXCEL_FILE, index=False, engine='openpyxl')
print(f"Data has been successfully exported to {config.EXCEL_FILE}")

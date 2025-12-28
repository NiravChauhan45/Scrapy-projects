import re
import pymongo
import pandas as pd
import xlsxwriter
import os
import config

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'ajio'
processed_collection_name = f'Product_details_{config.TODAY}'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[processed_collection_name]

df = pd.DataFrame(list(collection.find()))
df = df.drop(columns=['_id'], errors='ignore')

if 'product_id' in df.columns:
    df['product_id'] = df['product_id'].astype(str)

df.insert(0, 'Id', range(1, len(df) + 1))   # capital "Id" as per requirement

# cleaning functions
def remove_extra_space(text): return re.sub(r"\s+", " ", str(text)).strip()
def remove_duplicate(text): return " | ".join(set(str(text).split(" | ")))
def clean_category(text): return " | ".join(re.sub(r"\s+", " ", t).strip() for t in str(text).split("|"))

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

# Final header names exactly as you want in Excel
final_headers = [
    "Id", "product_id", "catalog_name", "catalog_id", "source", "scraped_date", "product_name",
    "Image_url", "category_heirarchy", "product_price", "arrival_date", "shipping_charges",
    "is_sold_out", "discount", "mrp", "page_url", "product_url", "number_of_ratings", "avg_rating",
    "position", "country_code", "images", "Best_Price","Best_offers", "bank_offer ",
    "product_details", "specifications", "rating", "MOQ", "brand", "product_code",
    "Available_sizes", "sellerPartnerId", "seller_return_policy", "manufacturing_info_packerInfo",
    "manufacturing_info_seller_name", "manufacturing_info_importerInfo",
    "manufacturing_info_countryOfOrigin", "manufacturing_info_manufacturerInfo",
    "More_colours", "variation Id"
]

# Agar column missing hoga to blank create hoga
df = df.reindex(columns=final_headers)

# Save Excel
if os.path.exists(config.EXCEL_FILE):
    os.remove(config.EXCEL_FILE)
    print(f"Existing file '{config.EXCEL_FILE}' removed.")

df.to_excel(config.EXCEL_FILE,index=False)
print(f"✅ Data has been successfully exported to {config.EXCEL_FILE}")

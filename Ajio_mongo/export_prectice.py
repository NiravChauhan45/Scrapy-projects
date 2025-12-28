import re
import pymongo
import pandas as pd
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
    "image_url", "category_hierarchy", "product_price", "arrival_date", "shipping_charges",
    "is_sold_out", "discount", "mrp", "page_url", "product_url", "number_of_ratings", "avg_rating",
    "position", "country_code", "images", "Best_price", "Best_offers", "bank_offers",
    "product_details", "specifications", "rating", "MOQ", "brand", "product_code",
    "Available_sizes", "sellerPartnerId", "seller_return_policy", "manufacturing_info_packerInfo",
    "manufacturing_info_seller_name", "manufacturing_info_importerInfo",
    "manufacturing_info_countryOfOrigin", "manufacturing_info_manufacturerInfo",
    "More_colours", "variation_id"
]

# Agar column missing hoga to blank create hoga
df = df.reindex(columns=final_headers)

# Save Excel with XlsxWriter
if os.path.exists(config.EXCEL_FILE):
    os.remove(config.EXCEL_FILE)
    print(f"Existing file '{config.EXCEL_FILE}' removed.")

with pd.ExcelWriter(config.EXCEL_FILE, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Products", index=False)

    # Access workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets["Products"]

    # Formatting examples
    header_format = workbook.add_format({"bold": True, "bg_color": "#D7E4BC"})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    worksheet.freeze_panes(1, 0)  # freeze header row
    worksheet.set_column("A:A", 6)   # Id
    worksheet.set_column("B:B", 20)  # product_id
    worksheet.set_column("G:G", 40)  # product_name
    worksheet.set_column("H:H", 50)  # image_url
    worksheet.set_column("I:I", 50)  # category_hierarchy
    worksheet.set_column(0, len(df.columns)-1, 25)  # default width for all

print(f"✅ Data has been successfully exported to {config.EXCEL_FILE} (using XlsxWriter)")

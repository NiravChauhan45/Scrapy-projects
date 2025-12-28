import pandas as pd

from pymongo import MongoClient
import config as db

# excel_file_path = 'client_inputs/ajio_nua_input_11_09_2025.xlsx'  # todo
excel_file_path = 'client_inputs/ajio_nua_input_29_09_2025.xlsx'  # todo
# df = pd.read_excel(excel_file_path, sheet_name='Ajio')
df = pd.read_excel(excel_file_path, sheet_name='Ajio')

try:
    product_ids = df['Ajio ID'].dropna()  # Drop any NaN values
except:
    product_ids = df['Ajio front ID'].dropna()  # Drop any NaN values

client = MongoClient('mongodb://localhost:27017/')
db_name = client[db.DB_NAME]
collection = db_name[db.COLLECTION_NAME]  # todo

for product_id in product_ids:
    if "-" not in str(product_id) or "" not in str(product_id).strip():
        # print(product_id)
        collection.update_one(
            {"product_id": product_id},
            {"$set": {"product_id": product_id, "status": "pending"}},
            upsert=True
        )

print("Data imported successfully!")

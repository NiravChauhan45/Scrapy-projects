import pandas as pd
from pymongo import MongoClient
import config as db
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='actowiz',
    database='ajio',
)

cur = conn.cursor()

excel_file_path = 'client_inputs/Ajio_NSM_12_09_2025.xlsx'  # todo
# excel_file_path = 'client_inputs/Ajio_input.xlsx'  # todo
# df = pd.read_excel(excel_file_path, sheet_name='osm-nsm')
# df = pd.read_excel(excel_file_path, sheet_name='nsm')
df = pd.read_excel(excel_file_path, sheet_name='nsm1')

try:
    product_ids = df['Product id'].dropna()  # Drop any NaN values
except:
    product_ids = df['Ajio front ID'].dropna()  # Drop any NaN values

client = MongoClient('mongodb://localhost:27017/')
db_name = client[db.DB_NAME]
collection = db_name[db.COLLECTION_NAME]  # todo

for product_id in product_ids:
    # try:
    #     sql = "INSERT INTO product_ids_22_09_2025 (product_id) VALUES (%s)"
    #     cur.execute(sql, (product_id))
    #     conn.commit()
    # except Exception as e:
    #     print(e)

    collection.update_one(
        {"product_id": product_id},
        {"$set": {"product_id": product_id, "status": "pending"}},
        upsert=True
    )
# conn.close()
print("Data imported successfully!")

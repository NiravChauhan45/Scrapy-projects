import os
from datetime import datetime

#Todo: MongoDB Configuration
# MONGO_URI = 'mongodb://localhost:27017/'  # MongoDB connection URI




TODAY = datetime.now().strftime("%d_%m_%Y")

DB_NAME = 'ajio'  # Todo: Database name

input_name = "OSM_NSM" # 1st & 3rd Monday of every month
# input_name = "NSM" # 2nd & 4th Monday of every month

input_sheetname = f'product_ids_{TODAY}'  # Collection name #todo

data_table_name = f'Product_details_{TODAY}'

# export_path = f"E:\\Nirav\\Project_export_data\\ajio\\{TODAY}\\"
export_path = f"E:\\Nirav\\Project_export_data\\ajio\\{TODAY}"

os.makedirs(export_path, exist_ok=True)

EXCEL_FILE = export_path + f"Ajio_{TODAY}.xlsx"


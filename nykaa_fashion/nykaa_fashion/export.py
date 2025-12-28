import os.path
from datetime import datetime

import numpy as np
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="nykaa_fashion"
)

today_date = datetime.now().strftime("%d_%m_%Y")

# sql_query = "select * from pdp_data;"
sql_query = "select * from pdp_data;"
df = pd.read_sql(sql_query, conn)
excel_path = "F:\\Nirav\\Project_export_data\\nykaa_fashion\\"

os.makedirs(excel_path, exist_ok=True)

excel_path = excel_path + f"nykaa_fashion_{today_date}.xlsx"

# df = df.rename(
#     columns={"id": "Sr.No", "city_name": "city", "date_of_scrap": "scrapeTimeAndDate", "product_id": "productId",
#              "Brand_Name": "brandName", "categories": "categoryName", "Product_Name": "productName",
#              "Product_Url": "productUrl",
#              "images_urls": "productImage", "Product_mrp": "mrp", "Product_Price": "productPrice", "InStock": "instock",
#              "Max_Quantity": "quantity", "variationId": "variationId",
#              "hash_key": "page_save_id"})
# df['content_of_reviews'] = df['content_of_reviews'].apply(lambda x: x.replace('[]', 'NA'))
# df = df.fillna("NA")
df = df.replace('', np.nan).fillna("N/A")
df.to_excel(excel_path, index=False, engine="openpyxl")
# df.to_csv(excel_path, index=False)

print(f"Your excel file has been generated, total count is: {df['S.No.'].count()}")

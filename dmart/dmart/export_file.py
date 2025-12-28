from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

# Example for MySQL:
engine = create_engine('mysql+pymysql://root:actowiz@localhost/new_dmart')

# query = "SELECT * FROM new_product_data"
query = "SELECT * FROM product_data"

df = pd.read_sql(query, engine)

current_date = datetime.now().strftime("%d_%m_%Y")

excel_file_path = f'D:\\Nirav_live_project_export_data\\dmart\\dmart_{current_date}.xlsx'


df = df.drop(
    ['city_name', 'main_category_name', 'sub_category_name', 'child_category_name', 'sku_unique_id', 'new_hash_key'],
    axis=1)
df.to_excel(excel_file_path, index=False)

print(f"Data has been successfully exported to {excel_file_path}")

#
# import pandas as pd
#
# df = pd.read_excel("D:\\Nirav Live Projects\\dmart\\dmart\\data\\dmart_24_09_2024.xlsx")
# df['Name'].replace(' ', '')
#
# print(df)

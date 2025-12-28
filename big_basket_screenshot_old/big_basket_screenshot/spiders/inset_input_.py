# import pandas as pd
# import hashlib
# import pymysql
# from datetime import datetime
#
# # ✅ CONFIGURATION
# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "actowiz",
#     "database": "big_basket_screenshot",
#     "charset": "utf8mb4"
# }
#
# # 📅 Generate today's date
# today_date = datetime.now().strftime('%d_%m_%Y')
#
# # 📂 Define paths
# data_path = f"D:\\Nirav Chauhan\\code\\big_basket_screenshot\\input\\{today_date}\\{today_date}.xlsx"
# pincode_path = f"D:\\Nirav Chauhan\\code\\big_basket_screenshot\\input\\Pincode\\pincode.xlsx"
#
# # 🚫 Ignore columns for hash generation
# ignore_columns = {
#     'Status', 'hash_id',
#     'Zepto', 'Zepto --  Approved/ Not Approved',
#     'Swiggy', 'Swiggy --  Approved/ Not Approved',
#     'Flipkart grocery', 'Flipkart Grocery --  Approved/ Not Approved',
#     'D-mart', 'Dmart --  Approved/ Not Approved',
#     'Blinkit', 'Blinkit --  Approved/ Not Approved',
#     # 'Bigbasket', 'BigBasket --  Approved/ Not Approved',
#     'Vishal Mega Mart', 'Vishal Mega Mart --  Approved/ Not Approved',
#     'Amazon Fresh', 'Amazon Fresh --  Approved/ Not Approved',
#     'Jiomart', 'Jiomart --  Approved/ Not Approved',
# }
#
# # ✅ Read Excel files
# all_df = pd.read_excel(data_path, sheet_name='Sheet1')
# city_df = pd.read_excel(pincode_path, sheet_name='CITY_AND_PINCODE')
#
# # 🛠 Rename the column to new name
# all_df.rename(columns={"BigBasket -- Approved/ Not Approved": "Bigbasket_correction"}, inplace=True)
#
# # 🔀 Cross join
# all_df['key'] = 1
# city_df['key'] = 1
# mapped_df = pd.merge(all_df, city_df, on='key').drop(columns=['key'])
#
# # 🔐 Generate hash_id
# def generate_hash(row):
#     filtered = {k: str(v).strip() for k, v in row.items() if k not in ignore_columns}
#     hash_input = '|'.join([filtered[col] for col in sorted(filtered.keys())])
#     return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
#
# mapped_df["Status"] = "pending"
# mapped_df["hash_id"] = mapped_df.apply(generate_hash, axis=1)
#
# # 🧱 MySQL Table Creation
# conn = pymysql.connect(**db_config)
# cursor = conn.cursor()
# cursor.execute(f"""
# CREATE TABLE IF NOT EXISTS `pdp_link_table_{today_date}` (
#   `Id` INT NOT NULL AUTO_INCREMENT,
#   `Name_Of_the_Brand` LONGTEXT,
#   `Category` LONGTEXT,
#   `Name_of_the_Product` LONGTEXT,
#   `Quantity_of_the_Product` LONGTEXT,
#   `Single_Pack` LONGTEXT,
#   `Bundle_Pack` LONGTEXT,
#   `Quantity` LONGTEXT,
#   `Packaging_of_the_product` LONGTEXT,
#   `big_basket` LONGTEXT,
#   `Bigbasket_correction` LONGTEXT,
#   `City_Name` LONGTEXT,
#   `zipcode` VARCHAR(20),
#   `Status` VARCHAR(255) DEFAULT 'pending',
#   `quantity_caping` VARCHAR(255),
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
# """)
#
#
# # # 📥 Insert into table (hash_id second last, Status last)
# # table_cols = [
# #     'Category', 'Name_Of_the_Brand', 'Quantity_of_the_Product', 'Single_Pack',
# #     'Bundle_Pack', 'Quantity_of_the_Product', 'Quantity', 'Packaging_of_the_product',
# #     'big_basket', 'City_Name', 'zipcode', 'Bigbasket_correction',
# #     'quantity_caping', 'Status'
# # ]
#
# table_cols = [
#
#     "Name_Of_the_Brand",
#     "Category",
#     "Name_of_the_Product",
#     "Quantity_of_the_Product",
#     "Single_Pack",
#     "Bundle_Pack",
#     "Quantity",
#     "Packaging_of_the_product",
#     "big_basket",
#     "Bigbasket_correction",
#     "City_Name",
#     "zipcode",
#     "Status",
#     "quantity_caping"
# ]
#
# # ✅ INSERT with backticks
# cols_with_backticks = ', '.join(f"`{col}`" for col in table_cols)
# placeholders = ', '.join(['%s'] * len(table_cols))
#
# insert_sql = f"""
# INSERT INTO `pdp_link_table_{today_date}`
# ({cols_with_backticks})
# VALUES ({placeholders})
# """
#
# # ✅ Clean NaNs to 'N/A'
# clean_df = mapped_df[table_cols].fillna("N/A").astype(str)
# data_to_insert = clean_df.values.tolist()
#
# # 🚀 Insert data
# try:
#     cursor.executemany(insert_sql, data_to_insert)
#     conn.commit()
#     print(f"✅ Inserted {cursor.rowcount} rows into `pdp_link_table_{today_date}`.")
# except Exception as e:
#     print("❌ Error inserting data:", e)
#     conn.rollback()
#
# cursor.close()
# conn.close()

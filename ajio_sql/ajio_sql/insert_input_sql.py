import pandas as pd
import pymysql
from loguru import logger
import db_config as db

db_connection = pymysql.connect(
    host='localhost',
    user='root',
    password='actowiz',
    database='ajio',
)

cursor = db_connection.cursor()


try:
    # SQL query to create the table if it does not exist
    create_table_query = f"""
        CREATE TABLE `{db.input_name}_inputs` (
          `id` int NOT NULL AUTO_INCREMENT,
          `product_id` varchar(100) DEFAULT NULL,
          `status` varchar(100) DEFAULT 'Pending',
          PRIMARY KEY (`id`),
          UNIQUE KEY `product_id` (`product_id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=8010 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """
    # Execute the SQL command
    cursor.execute(create_table_query)
    db_connection.commit()
    print("Table checked and created if not exists.")
except Exception as error:
    logger.error(error)



excel_file_path = fr'D:\Nirav Chauhan\Code\ajio_sql\ajio_sql\client_inputs\Ajio_{db.input_name}_10_10_2025.xlsx'  # todo
try:
    df = pd.read_excel(excel_file_path, sheet_name='NSM')
except:
    df = pd.read_excel(excel_file_path, sheet_name='OSM_NSM')

try:
    product_ids = df['Product id'].dropna()  # Drop any NaN values
except:
    product_ids = df['Ajio front ID'].dropna()  # Drop any NaN values

for product_id in product_ids:
    try:
        sql = fr"INSERT INTO {db.input_name}_inputs (product_id) VALUES (%s)"
        # sql = "INSERT INTO nsm_inputs (product_id) VALUES (%s)"
        cursor.execute(sql, (product_id))
        db_connection.commit()
        print(f"{product_id} inserted successfully..!")
    except Exception as e:
        print(e)

print("Data imported successfully!")

db_connection.close()

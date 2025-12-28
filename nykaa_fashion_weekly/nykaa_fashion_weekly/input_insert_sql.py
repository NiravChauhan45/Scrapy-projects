from loguru import logger
import pymysql
import pandas as pd
import db_config as db

db_connection = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database=db.database_name,
)
cursor = db_connection.cursor()

try:
    # SQL query to create the table if it does not exist
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{db.link_table}` (
          `id` int NOT NULL AUTO_INCREMENT,
          `product_id` varchar(100) DEFAULT NULL,
          `product_url` varchar(255) DEFAULT NULL,
          `status` varchar(100) DEFAULT 'Pending',
          PRIMARY KEY (`id`),
          UNIQUE KEY `product_id` (`product_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """

    # Execute the SQL command
    cursor.execute(create_table_query)
    db_connection.commit()
    print("Table checked and created if not exists.")
except Exception as error:
    logger.error(error)

osm_nsm_filepath = fr"E:\Nirav\Project_code\nykaa_fashion_weekly\nykaa_fashion_weekly\client_inputs\{db.input_name}_10_10_2025.xlsx"

df = pd.read_excel(osm_nsm_filepath)

for product_id in df['Nykaa Fashion']:
    product_id = str(product_id)
    if '.' in product_id:
        product_id = product_id.split('.')[0]

    product_id = product_id.replace("nan", "")

    if str(product_id).strip():
        print(product_id)
        product_url = f"https://www.nykaafashion.com/%20/p/{product_id}"
        sql = f"INSERT IGNORE INTO {db.link_table} (product_id, product_url) VALUES (%s, %s)"
        cursor.execute(sql, (product_id, product_url))
        print("Data inserted successfully...")
        db_connection.commit()
db_connection.close()

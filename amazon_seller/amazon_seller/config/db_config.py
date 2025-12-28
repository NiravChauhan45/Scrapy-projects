import pymysql
from datetime import datetime

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="amazon_s"
)

delivery_date = datetime.now().strftime("%d_%m_%Y")

database_name = "amazon_s"
product_link_table = "product_links"
variation_id_table = "variation_id_table"
item_table_name = "item_table"




"""
SELECT *
FROM `product_data_20250711`
ORDER BY 
  CAST(SUBSTRING_INDEX(sr_nos_2, '.', 1) AS UNSIGNED),       -- major version
  CAST(SUBSTRING_INDEX(sr_nos_2, '.', -1) AS UNSIGNED);      -- minor version
COMMIT; 
"""
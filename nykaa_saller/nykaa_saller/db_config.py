from datetime import datetime
import pymysql

# current_date = datetime.now().strftime("%d_%m_%Y")
current_date = "16_12_2025"

database_name = 'nykaa_seller'
link_table = 'pdp_links'
pdp_table = f"pdp_data_{current_date}"
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database=database_name
)

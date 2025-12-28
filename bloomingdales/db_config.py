from datetime import datetime
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="bloomingdales"
)

cursor = connection.cursor()

# current_date = datetime.now().strftime("%d_%m_%Y")
current_date = "29_11_2025"
database_name = "bloomingdales"
pdp_links = "pdp_links"
category_links = "category_links"
pdp_data = f"pdp_data_{current_date}"
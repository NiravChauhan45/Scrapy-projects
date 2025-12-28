from datetime import datetime
import pymysql

# current_date = datetime.now().strftime("%d_%m_%Y")
current_date = "15_12_2025"
database_name = 'reformation_new'
pdp_links_sitemap = 'pdp_links_sitemap'
category_table = 'category_links'
pdp_links = 'pdp_links'
pdp_data = f"pdp_data_{current_date}"
variations_links = f"variations_links"
product_links = "product_links"


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database=database_name
)
cursor = connection.cursor()

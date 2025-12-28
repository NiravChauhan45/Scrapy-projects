from datetime import datetime

# Todo: delivery date
# delivery_date = datetime.now().strftime("%Y-%m-%d")
# delivery_date = "2025_01_20"
delivery_date = "2025_02_05"

# Todo: pipline
host = 'localhost'
username = 'root'
password = 'actowiz'
database_name = "Deliveroo_HK"
geohash_data = f"geohash_data"
restaurant_links = f"restaurant_links_{delivery_date}"
deliveroo_restaurant = f"deliveroo_restaurant_{delivery_date}"
data_menu_delivery = f"data_menu_delivery_{delivery_date}"
data_menu_pickup = f"data_menu_pickup_{delivery_date}"

# Todo: pagesave path
# pagesave_date = "2025-01-20"
pagesave_date = "2025-02-05"
geohash_path = f"E:\\PAGESAVE\\Nirav Chauhan\\{database_name}\\{pagesave_date}\\Geohash_new\\"
pagesave_cart_path = f"E:\\PAGESAVE\\Nirav Chauhan\\{database_name}\\{pagesave_date}\\Cart\\"
pagesave_data_path = f"E:\\PAGESAVE\\Nirav Chauhan\\{database_name}\\{pagesave_date}\\Data\\"
pagesave_review_count_path = f"E:\\PAGESAVE\\Nirav Chauhan\\{database_name}\\{pagesave_date}\\Review_Count\\"
pagesave_collection_request_path = f"E:\\PAGESAVE\\Nirav Chauhan\\{database_name}\\{pagesave_date}\\Collection_Request\\"
menu_store_delivery_path = f"E:\\PAGESAVE\\Nirav Chauhan\\{database_name}\\{pagesave_date}\\Menu_Store_Delivery\\"
menu_store_pickup_path = f"E:\\PAGESAVE\\Nirav Chauhan\\{database_name}\\{pagesave_date}\\Menu_Store_Pickup\\"

# Todo: Filepath
# filedate = "20012025"
filedate = "05022025"
filedate1 = "20250205"
file_path = f'D:\\DATA\\Nirav Chauhan\\DATA\\aniket bhai\\{database_name}\\{pagesave_date}\\'
csv_file_name = f"Deliveroo_{filedate}.csv"
csv_menu_full_file_name = f"Deliveroo_{filedate1}_menu_full_file.csv"
csv_menu_full_file_name_with_count = f"Deliveroo_{filedate1}_menu_full_file_with_count.csv"

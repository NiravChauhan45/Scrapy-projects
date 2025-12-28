import datetime

current_date = datetime.datetime.now().strftime("%d_%m_%Y")
filepath = fr'D:\Nirav Chauhan\Data\Amazon_Fresh_Screenshot\{current_date}'
amazon_filename = fr"Amazon_fresh_data_{current_date}"
pdp_data_table = f"pdp_data_{current_date}"
pdp_link_table = f"pdp_link_table"

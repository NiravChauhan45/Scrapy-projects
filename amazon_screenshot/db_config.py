import datetime

current_date = datetime.datetime.now().strftime("%d_%m_%Y")
# screenshot_filepath = fr"D:\Nirav Chauhan\screenshot\Amazon_Fresh_Screenshot\{current_date}"
# pagesave_filepath = fr"D:\Nirav Chauhan\Pagesave\Amazon_Fresh_Screenshot\{current_date}"
# data_filepath = fr"D:\Nirav Chauhan\Data\Amazon_Fresh_Screenshot\{current_date}"

screenshot_filepath = fr"E:\Nirav\Project_screenshot\Amazon_Fresh_Screenshot\{current_date}"
pagesave_filepath = fr"E:\Nirav\Project_page_save\Amazon_Fresh_Screenshot\{current_date}"
data_filepath = fr"E:\Nirav\Project_export_data\Amazon_Fresh_Screenshot\{current_date}"

database_name = "amazon_fresh_screenshot"

amazon_filename = fr"Amazon_fresh_data_{current_date}"
pincode_table = "pincode_table"
pdp_link_table = f"pdp_link_table_09_09_2025"
pdp_data_table = f"pdp_data_{current_date}"

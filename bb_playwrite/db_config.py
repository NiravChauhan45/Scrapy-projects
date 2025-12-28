import datetime

current_date = datetime.datetime.now().strftime("%d_%m_%Y")
# current_date = "11_04_2025"

filepath = r"F:\Nirav\Project_code\bb_playwrite\output_files"
amazon_filename = fr"Amazon_fresh_data_{current_date}"
big_basket_filename = fr"big_basket_data_{current_date}"

amazon_pdp_table = f"pdp_data_{current_date}"
big_basket_pdp_table = f"pdp_data_{current_date}"

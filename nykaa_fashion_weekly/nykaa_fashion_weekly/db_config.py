import os
from datetime import datetime

current_date = datetime.now().strftime("%d_%m_%Y")
# current_date = "24_10_2025"

# input_name = "OSM_NSM"  # 1st & 3rd Monday of every month
input_name = "NSM" # 2nd & 4th Monday of every month


output_filename = f"Nykaa_fashion_{input_name}_{current_date}.xlsx"
database_name = "nykaa_fashion"
collection_name = f"pdp_data_{current_date}"

link_table = f"{current_date}_{input_name}"
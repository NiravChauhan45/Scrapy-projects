import os
import json

import numpy as np
import pandas as pd
from datetime import datetime
import db_config as db


def update_sku_packshot(excel_path, json_path):
    # Read Excel file
    df = pd.read_excel(excel_path)

    # Load JSON with SKU Packshot links
    try:
        with open(json_path, 'r') as f:
            uploaded_files = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        uploaded_files = {}

    # Update 'SKU Packshot' column with corresponding values from JSON
    if 'SKU Packshot' in df.columns:
        df['SKU Packshot'] = df['SKU Packshot'].apply(lambda x: uploaded_files.get(str(x).strip(), x))
    else:
        print("⚠️ 'SKU Packshot' column not found in the Excel file.")

    # Save the updated file
    updated_path = excel_path.replace('.xlsx', '_updated.xlsx')
    df.replace('', 'N/A', inplace=True)
    df.replace(np.nan, 'N/A', inplace=True)
    df.to_excel(updated_path, index=False)
    print(f"✅ Updated file saved at: {updated_path}")


# Example usage
if __name__ == '__main__':
    # Set your file paths here
    today_local = datetime.now().strftime('%d_%m_%Y')
    excel_file = f"D:\\Nirav Chauhan\\Data\\Big_Basket_Screenshot\\{db.current_date}\\Big_Basket_data_{db.current_date}.xlsx"
    json_file = f"D:\\Nirav Chauhan\\screenshot\\Big_Basket_Screenshot\\{db.current_date}\\uploaded_links.json"

    update_sku_packshot(excel_file, json_file)

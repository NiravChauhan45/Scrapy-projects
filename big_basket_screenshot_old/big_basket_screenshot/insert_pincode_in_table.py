import datetime
import os
import pandas as pd

current_date = datetime.datetime.now().strftime('%d_%m_%Y')

def map_all_rows(file_path, output_file):
    """
    Reads an Excel file with two sheets ('Sheet1' and 'Sheet2') and maps all rows
    from Sheet1 with all rows from Sheet2. Saves the result to a new CSV file.
    """
    # Load the Excel file
    xls = pd.ExcelFile(file_path)
    print("Available sheets:", xls.sheet_names)

    # Adjust if needed
    sheet1 = pd.read_excel(xls, 'Sheet1')
    sheet2 = pd.read_excel(xls, 'Sheet2')

    # Perform a cross join (compatible with all pandas versions)
    sheet1['key'] = 1
    sheet2['key'] = 1
    mapped_data = pd.merge(sheet1, sheet2, on='key').drop('key', axis=1)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save result
    mapped_data.to_csv(output_file, index=False)
    print(f"✅ Mapped data has been saved to: {output_file}")

# Paths
input_filepath = r"E:\Nirav\Project_code\big_basket_screenshot\big_basket_screenshot\big_basket_screenshot\input\08_09_2025\08_09_2025.xlsx"
Output_filepath = r"E:\Nirav\Project_code\big_basket_screenshot\big_basket_screenshot\big_basket_screenshot\output\08_09_2025\08_09_2025.csv"

# Run
map_all_rows(input_filepath, Output_filepath)

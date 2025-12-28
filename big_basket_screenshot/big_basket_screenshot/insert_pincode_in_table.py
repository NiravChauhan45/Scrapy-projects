import datetime
import os

import pandas as pd

current_date = datetime.datetime.now().strftime('%d_%m_%Y')

def map_all_rows(file_path, output_file):
    """
    Reads an Excel file with two sheets ('Sheet1' and 'Sheet2') and maps all rows
    from Sheet1 with all rows from Sheet2. Saves the result to a new CSV file.
    Args:
        file_path (str): Path to the input Excel file.
        output_file (str): Path to save the output CSV file.
    Returns:
        None: Saves the mapped data to a new CSV file.
    """
    # Load the Excel file
    xls = pd.ExcelFile(file_path)
    # Read the sheets
    sheet1 = pd.read_excel(xls, 'Sheet1')
    sheet2 = pd.read_excel(xls, 'Sheet2')
    # Perform a cross join (Cartesian product)
    mapped_data = sheet1.merge(sheet2, how='cross')
    # Save the mapped data to a new CSV file
    mapped_data.to_csv(output_file, index=False)
    print(f"Mapped data has been saved to: {output_file}")

input_filepath = fr"..\input\{current_date}"
Output_filepath = fr"..\Output\{current_date}"
os.makedirs(input_filepath,exist_ok=True)
os.makedirs(Output_filepath,exist_ok=True)
# Example usage
input_filepath = fr"{input_filepath}\{current_date}.xlsx"  # Input Excel file
Output_filepath = fr"{Output_filepath}\{current_date}.csv"  # Output CSV file
# Call the function
map_all_rows(input_filepath, Output_filepath)

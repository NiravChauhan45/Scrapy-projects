import pandas as pd


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


# Example usage
file_path = r"F:\Nirav\Project_code\bb_playwrite\output_files\big_basket_input_data_15_04_2025.xlsx"  # Input Excel file
output_file = r"F:\Nirav\Project_code\bb_playwrite\output_files\big_basket_input_data_15_04_2025.csv"  # Output CSV file
# Call the function
map_all_rows(file_path, output_file)

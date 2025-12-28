import pandas as pd

# Load the CSV file
csv_file = r"F:\Nirav\Project_code\amazon_momcozy\amazon_momcozy\csv_files\main_csv.csv"  # Change this to your CSV file path
df = pd.read_csv(csv_file)

# Remove duplicate rows
df = df.drop_duplicates()

# Add a new ID column starting from 1
df.insert(0, "ID", range(1, len(df) + 1))

# Save the cleaned DataFrame to an Excel file
df.to_excel("output.xlsx", index=False, engine="openpyxl")

print("CSV converted to Excel, duplicates removed, and ID column added successfully!")

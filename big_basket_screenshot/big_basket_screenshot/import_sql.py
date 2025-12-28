import re
from datetime import datetime
import zipfile
import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
# Path to the Downloads folder where the Excel file is located
downloads_folder = 'C:\\Users\\Administrator\\Downloads'

# Get the list of all Excel files in the Downloads folder
excel_files = [f for f in os.listdir(downloads_folder) if f.endswith('.xlsx') or f.endswith('.xls')]

if excel_files:
    # Find the latest Excel file based on its creation time
    latest_file = max(excel_files, key=lambda x: os.path.getctime(os.path.join(downloads_folder, x)))
    print("Latest Excel file:", latest_file)

    # Full path of the latest Excel file
    file_path = os.path.join(downloads_folder, latest_file)

    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Get today's date in the format YYYY_MM_DD for the table name
    today_date = datetime.today().strftime('%Y_%m_%d')

    # MySQL connection details
    host = '172.27.131.182'
    user = 'root'
    password = 'actowiz'
    database = 'big_basket_screenshot'

    # Create SQLAlchemy engine for MySQL
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

    # Insert the DataFrame into the SQL database, creating a table with today's date in th
    # e name
    df.to_sql(name=f'update', con=engine, if_exists='replace', index=False)
    print("Data has been inserted into the SQL database successfully!")
else:
    print("No Excel files found in the Downloads folder.")
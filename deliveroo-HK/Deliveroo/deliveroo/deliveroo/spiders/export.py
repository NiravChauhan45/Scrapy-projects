import os
import re

import mysql.connector
import numpy as np
import pandas as pd
import deliveroo.df_config as db

# Todo: This file is use for restaurant data export

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)


def row_average_include_zero(row):
    # Filter out only NaN values
    try:
        row = row.split("|=|")[0]
    except:
        row = row
    return row


def export():
    import pandas as pd
    import pymysql

    # Connect to your MySQL database
    connection = pymysql.connect(
        host=db.host,
        user=db.username,
        password=db.password,
        database=db.database_name
    )
    # file_path = 'C:\\Deliveroo\\21012025\\'
    file_path = db.file_path
    os.makedirs(file_path, exist_ok=True)

    # if os.path.exists(file_path):
    #     print("Directory ", file_path, " already exists")
    # else:
    #     os.mkdir(file_path)
    #     print("Directory ", file_path, " Created ")

    # SQL query to select data from a table
    sql_query = f'SELECT * FROM {db.deliveroo_restaurant}'#deliveroo_restaurant_2025_01_21

    df = pd.read_sql_query(sql_query, connection)
    df['name'] = df['name'].str.decode('utf-8')
    df['name_local'] = df['name_local'].str.decode('utf-8')
    df['branch_name'] = df['branch_name'].str.decode('utf-8')
    df['others'] = df['others'].str.decode('utf-8').replace("\n", "").replace("\r", "").replace("\t", "")

    df['branch_name_local'] = df['branch_name_local'].str.decode('utf-8')
    df['category'] = df['category'].str.decode('utf-8').replace("", " ").replace("\n", "").replace("\r", "").replace(
        "\t", "")
    try:
        df['category'] = df['category'].apply(row_average_include_zero)
    except:
        pass
    # df['category'] = df['category'].str.decode('utf-8').replace("\\n"," ").replace("","").replace("","").replace("","").replace("","")

    # df['category'] = pd.Series(clean_text(str (item)) for item in df['category'])

    df.drop(columns=['status'], inplace=True)
    df['delivery_time'] = df['delivery_time'].astype(str)
    connection.close()

    # Export the DataFrame to a CSV file
    # df.to_excel(f'{file_path}output.xlsx', index=False, engine='openpyxl')
    df.to_csv(f'{file_path}{db.csv_file_name}', index=False,
              encoding='utf-8-sig')  # Replace 'output_file.csv' with your desired CSV file name


if __name__ == '__main__':
    export()

    # scraped_id

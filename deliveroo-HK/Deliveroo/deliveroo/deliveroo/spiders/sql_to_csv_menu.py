import os

import pandas as pd
import mysql.connector
import deliveroo.df_config as db


def export_menu():
    # Connect to your MySQL database
    connection = mysql.connector.connect(
        host=db.host,
        user=db.username,
        password=db.password,
        database=db.database_name
    )

    # SQL query to select data from a table
    sql_query = f'SELECT * FROM {db.data_menu_delivery}'  # data_menu_delivery_2025_01_21

    # file_path = 'C:\\Deliveroo\\21012025\\'
    file_path = db.file_path
    os.makedirs(file_path, exist_ok=True)

    # Use pandas to read the SQL query result into a DataFrame
    df = pd.read_sql_query(sql_query, connection)
    df['menu_items'] = df['menu_items'].str.decode('utf-8')
    df['menu_Category'] = df['menu_Category'].str.decode('utf-8')

    df.drop(columns=['hashid'], inplace=True)
    # df.drop(columns=['shopName'], inplace=True)
    df['original_price_Delivery'].fillna(0, inplace=True)
    df['original_price_Delivery'].replace('NA', 0, inplace=True)

    df['discounted_price_Delivery'].fillna(0, inplace=True)
    df['discounted_price_Delivery'].replace('NA', 0, inplace=True)

    df['discount_price_Delivery'].fillna(0, inplace=True)
    df['discount_price_Delivery'].replace('NA', 0, inplace=True)

    df['discount_MOV_Delivery'].fillna(0, inplace=True)
    df['discount_MOV_Delivery'].replace('NA', 0, inplace=True)

    df['original_price_pickup'].fillna(0, inplace=True)
    df['original_price_pickup'].replace('NA', 0, inplace=True)

    df['discounted_price_pickup'].fillna(0, inplace=True)
    df['discounted_price_pickup'].replace('NA', 0, inplace=True)

    df['discount_price_pickup'].fillna(0, inplace=True)
    df['discount_price_pickup'].replace('NA', 0, inplace=True)

    df['discount_MOV_pickup'].fillna(0, inplace=True)
    df['discount_MOV_pickup'].replace('NA', 0, inplace=True)
    df['date_of_scrape'].replace(' 00:00:00', '', inplace=True)
    df['date_of_data_inserted'].replace(' 00:00:00', '', inplace=True)
    df.fillna("NA", inplace=True)

    # Todo: uncomment this below code when you generating Deliveroo_20250205_menu_full_file_with_count.csv.csv
    group_df=df.groupby(['vendor_id','menu_Category'])
    result_df=pd.DataFrame()
    count=0
    for _,group in group_df:
        count+=1
        print("Count",count)
        cat_name=group['menu_Category'].iloc[0]
        cat_count=len(group)
        group['Category Counts'] =cat_count
        print("Category Counts",group['Category Counts'])
        result_df=result_df._append(group)

    # Close the database connection
    connection.close()

    # Todo: Export the DataFrame to a CSV file
    # Todo: comment this below code when you generating Deliveroo_20250205_menu_full_file_with_count.csv
    # df.to_csv(f'{file_path}{db.csv_menu_full_file_name}', index=False,
    #           encoding='utf-8-sig')

    # Todo: uncomment this below code when you generating Deliveroo_20250205_menu_full_file_with_count.csv.csv
    result_df.to_csv(f'{file_path}{db.csv_menu_full_file_name_with_count}', index=False,
              encoding='utf-8-sig')
    print("File successfully generated..!!")


if __name__ == '__main__':
    export_menu()

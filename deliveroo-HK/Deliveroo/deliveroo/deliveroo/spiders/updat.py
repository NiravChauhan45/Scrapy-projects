# import geopy
# import mysql.connector
# import pandas as pd
# from geopy.geocoders import Nominatim
# import geohash2 as geohash
# import numpy as np
#
#
#
#
# def main_data():
#     df = pd.read_excel('deliveroo_missing_data.xlsx')
#     latitudes = df['latitude']
#     longitudes = df['longitude']
#
#     # Print the first few latitude and longitude values
#     df['geo_hash'] = [geohash.encode(lat, lon) for lat, lon in zip(latitudes, longitudes)]
#     df.to_excel("updated_file.xlsx", index=False)  # Save to Excel without row indices
#
#
# if __name__ == "__main__":
#     main_data()



import pandas as pd
import pymysql

def export_menu():
    # Connect to your MySQL database
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='actowiz',
        database='deliveroo'
    )

    # SQL query to select data from a table
    sql_query = 'SELECT * FROM data_menu_delivery_2024_11_07'

    file_path = 'D:\\Deliveroo\\'

    # Use pandas to read the SQL query result into a DataFrame
    df = pd.read_sql_query(sql_query, connection)
    df['menu_items']=df['menu_items'].str.decode('utf-8')
    df['menu_Category']=df['menu_Category'].str.decode('utf-8')

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
    group_df=df.groupby(['vendor_id','menu_Category'])

    # result_df=pd.DataFrame()
    # count=0
    # for _,group in group_df:
    #     count+=1
    #     print("Count",count)
    #     cat_name=group['menu_Category'].iloc[0]
    #     cat_count=len(group)
    #     group['Category Counts'] =cat_count
    #     print("Category Counts",group['Category Counts'])
    #     result_df=result_df._append(group)
    # df['other   ']=df['branch_name'].str.decode('utf-8')

    # Close the database connection
    connection.close()

    # Export the DataFrame to a CSV file
    df.to_csv(f'{file_path}Deliveroo_20241111_menu_store_file.csv', index=False,encoding='utf-8-sig')  # Replace 'output_file.csv' with your desired CSV file name
if __name__ == '__main__':
    export_menu()

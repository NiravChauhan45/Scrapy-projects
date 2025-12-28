import pandas as pd
import pymysql

# Database connection details

# connection = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='actowiz',
#     database='amzone_image_data'
# )

# Load CSV file
csv_file = r'Z:\Vipul\apiFile\08032025\amazon_08032025update.csv'  # Your CSV file
df = pd.read_csv(csv_file)
print(df)
# Select specific columns (e.g., column1, column2, column3, column4)
#
# # # Insert data row by row
# for _, row in filtered_df.iterrows():
#     insert_query = '''
#     INSERT INTO my_table (column2, column3, column4)
#     VALUES (%s, %s, %s, %s)
#     '''
#     cursor.execute(insert_query, tuple(row))
#
# # # Commit and close connection
# # connection.commit()
# # cursor.close()
# # connection.close()
# # print("Data inserted successfully.")

import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='actowiz',
    database='kohinoor_electronics'
)

# cur = mydb.cursor()
select_query = "select * from product_data"

df = pd.read_sql(select_query, mydb)

filename = 'final_data.xlsx'

filepath = f'F:\\Nirav\\Project_code\\kohinoor_electronics\\{filename}'

df.to_excel(filepath, index=False, sheet_name='data')
df.to_excel(filepath, index=False, sheet_name='data')
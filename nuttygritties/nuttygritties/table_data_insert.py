import pandas as pd
import sqlalchemy
import pymysql

file_name = "F:\\Nirav Live Projects\\nuttygritties\\nuttygritiesinputs.xlsx"
xl = pd.ExcelFile(file_name)

mydb = pymysql.connect(host="localhost", user="root", password="actowiz", database="nuttygritties")
cur = mydb.cursor()
db_conn = sqlalchemy.create_engine("mysql+pymysql://root:actowiz@localhost/nuttygritties")
# amazon_search_input
for sheet_name in xl.sheet_names:
    df = pd.read_excel(file_name, sheet_name=sheet_name)
    table_name = sheet_name.lower().replace(" ", "_")  # Table name based on sheet name
    df_filled = df.fillna(' ')
    df_filled.to_sql(f'{table_name}_input', con=db_conn, if_exists='replace', index=False)

mydb.commit()
print("Tables inserted into the database.")
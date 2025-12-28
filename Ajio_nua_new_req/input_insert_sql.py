import pymysql
import pandas as pd

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="ajio_nua",
)
cursor = conn.cursor()
ajio_nua_input = r"E:\Nirav\Project_code\Ajio_nua\client_inputs\Ajio_input_01_09_2025.csv"

table_name = "ajio_input_01_09_2025"

df = pd.read_csv(ajio_nua_input)

for nykaa_fashion in df['Ajio ID']:
    nykaa_fashion = str(nykaa_fashion)
    if '.' in nykaa_fashion:
        nykaa_fashion = nykaa_fashion.split('.')[0]

    nykaa_fashion = nykaa_fashion.replace("nan", "")

    if str(nykaa_fashion).strip():
        print(nykaa_fashion)
        sql = f"INSERT IGNORE INTO {table_name} (Nykaa_Fashion) VALUES (%s)"
        cursor.execute(sql, (nykaa_fashion))
        print("Data inserted successfully...")
        conn.commit()
conn.close()

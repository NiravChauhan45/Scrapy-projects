# import pandas as pd
# import pymysql
#
# conn = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='actowiz',
#     database='big_basket_com'
# )
# table_name = 'pincodes'
#
# cursor = conn.cursor()
#
# pincode_dict = {
#     'Chennai': [
#         '600083'
#     ],
#     'Bangalore': [
#         '560034',
#         '560001'
#     ],
#     'Hyderabad': [
#         '500081'
#     ],
#     'Ahmedabad': [
#         '380054'
#     ],
#     'Nagpur': [
#         '440010'
#     ],
#     'Delhi': [
#         '110001',
#         '110016',
#         '110026',
#         '110092'
#     ],
#     'Mumbai': [
#         '400001',
#         '400013',
#         '400050',
#         '400101'
#     ],
#     'Kolkata': [
#         '700017',
#         '700019',
#         '700026',
#         '700034'
#     ],
#     'Lucknow': [
#         '226001',
#         '226004',
#         '226010',
#         '226021'
#     ],
#     'Patna': [
#         '800001',
#         '800002',
#         '800008',
#         '800013'
#     ]
# }
#
# for city_name, pincode_list in pincode_dict.items():
#     for pincode in pincode_list:
#         print(city_name, pincode)
#         query = f"INSERT INTO {table_name} (city, pincode) VALUES (%s, %s)"
#         values = (city_name, pincode)
#         cursor.execute(query, values)
#         print(f"{pincode} Inserted Successfully!")
# conn.commit()
# conn.close()

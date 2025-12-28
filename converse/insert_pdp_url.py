import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="converse_new"
)

cursor = conn.cursor()

sql_select = "SELECT product_url FROM pdp_links_backup"
cursor.execute(sql_select)

results = cursor.fetchall()

for result in results:
    sql = """
    INSERT IGNORE INTO pdp_links (product_url)
    VALUES (%s)
    """
    product_url = result[0]

    new_product_url = ''
    if 'Product-Variation' not in product_url:
        new_product_url = product_url.split('?')[0]

        values = (new_product_url)

        cursor.execute(sql, values)
        conn.commit()
        print('Intem Inserted Successfully..')

        sql = "UPDATE pdp_links_backup SET status = 'Done' WHERE product_url = %s"
        values = (product_url)

        cursor.execute(sql, values)
        conn.commit()
        print('Intem Updated Successfully..')
    else:
        new_product_url = product_url.split('&')[0]

        values = (new_product_url)

        cursor.execute(sql, values)
        conn.commit()
        print('Intem Inserted Successfully..')

        sql = "UPDATE pdp_links_backup SET status = 'Done' WHERE product_url = %s"
        values = (product_url)

        cursor.execute(sql, values)
        conn.commit()
        print('Intem Updated Successfully..')


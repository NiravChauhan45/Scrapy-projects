import datetime
import hashlib
import db_config as db
import mysql.connector

# Database connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="amazon_fresh_screenshot"
)

# Table names
select_table = 'pdp_link_table'
current_date = datetime.datetime.now().strftime("%d_%m_%Y")
insert_table = f"pdp_data_{current_date}"
cursor = connection.cursor()

# Todo: Update pl table
update_table = f"""UPDATE `{select_table}` SET STATUS = 'Pending'"""
cursor.execute(update_table)
connection.commit()

# Todo: Create pdp table
create_table = f"""
    CREATE TABLE `{db.amazon_pdp_data}` (
          `Sr.No` int NOT NULL AUTO_INCREMENT,
          `Portal Name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
          `Product Url` longtext,
          `Date (Crawler Date)` varchar(100) DEFAULT NULL,
          `Time (Crawler Time)` varchar(100) DEFAULT NULL,
          `City Name` varchar(255) DEFAULT NULL,
          `Pincode` varchar(100) DEFAULT NULL,
          `Brand` varchar(150) DEFAULT NULL,
          `Category` varchar(200) DEFAULT NULL,
          `SKU Packshot` varchar(200) DEFAULT NULL,
          `SKU Name` varchar(200) DEFAULT NULL,
          `Pack Size` varchar(200) DEFAULT NULL,
          `Single Pack` varchar(200) DEFAULT NULL,
          `Bundle Pack` varchar(200) DEFAULT NULL,
          `Per Gm Price (Unit Price)` varchar(20) DEFAULT NULL,
          `MRP` varchar(10) DEFAULT NULL,
          `Selling price` varchar(10) DEFAULT NULL,
          `Discount (%)` varchar(10) DEFAULT NULL,
          `Save Rs.` varchar(10) DEFAULT NULL,
          `Availability Status` varchar(30) DEFAULT NULL,
          `Quantity Caping` varchar(10) DEFAULT NULL,
          `Remarks` varchar(10) DEFAULT NULL,
          `Quantity` varchar(10) DEFAULT NULL,
          `Packaging of the product` varchar(40) DEFAULT NULL,
          `hash_id` varchar(50) DEFAULT NULL,
          PRIMARY KEY (`Sr.No`),
          UNIQUE KEY `hash_id` (`hash_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=481 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""
try:
    cursor.execute(create_table)
    connection.commit()
except Exception as e:
    print(e)
# Corrected table name reference
query = f"SELECT * FROM `{select_table}` WHERE `Amazon Fresh`='' AND STATUS='Pending'"
cursor.execute(query)
results = cursor.fetchall()

for result in results:
    id = result[0]
    new_category = result[1]
    name_of_the_brand = result[2]
    name_of_the_product = result[3]
    single_pack = result[4]
    bundle_pack = result[5]
    quentity_of_the_product = result[6]
    quantity = result[7]
    packing_of_the_product = result[8]
    product_url = result[9]
    new_zipcode = result[10]
    city_name = result[11]
    # Prepare item dictionary
    hash_id = str(
        int(hashlib.md5(bytes(
            str(new_category + new_zipcode + name_of_the_product), "utf8")).hexdigest(),
            16) % (
                10 ** 10))

    item = {
        "Sr.No": id,
        "Portal Name": "Amazon Fresh",
        "Product Url": product_url if product_url else 'N/A',
        "Date (Crawler Date)": datetime.datetime.now().strftime("%d-%m-%Y"),
        "Time (Crawler Time)": datetime.datetime.now().strftime("%H:%M"),
        "City Name": city_name,
        "Pincode": new_zipcode,
        "Brand": name_of_the_brand if name_of_the_brand else 'N/A',
        "Category": new_category if new_category else 'N/A',
        "SKU Packshot": 'N/A',
        "SKU Name": name_of_the_product if name_of_the_product else 'N/A',
        "Pack Size": quentity_of_the_product if quentity_of_the_product else 'N/A',
        "Single Pack": single_pack if single_pack else 'N/A',
        "Bundle Pack": bundle_pack if bundle_pack else 'N/A',
        "Per Gm Price (Unit Price)": 'N/A',
        "MRP": 'N/A',
        "Selling price": 'N/A',
        "Discount (%)": 'N/A',
        "Save Rs.": 'N/A',
        "Availability Status": 'Not listed',
        "Quantity Caping": 'N/A',
        "Remarks": "N/A",
        "Quantity": quantity if quantity else 'N/A',
        "Packaging of the product": packing_of_the_product if packing_of_the_product else 'N/A',
        "hash_id": hash_id
    }
    print(item)

    # Prepare insert query
    placeholders = ', '.join(['%s'] * len(item))
    columns = ', '.join([f"`{key}`" for key in item.keys()])
    sql = f"INSERT INTO {insert_table} ({columns}) VALUES ({placeholders})"

    try:
        cursor.execute(sql, list(item.values()))
        connection.commit()
    except Exception as e:
        print(f"Error inserting data for ID {id}: {e}")

    # Update status
    try:
        update_query = f"UPDATE {select_table} SET status='Done' WHERE id = %s"
        cursor.execute(update_query, (id,))
        connection.commit()
    except Exception as e:
        print(f"Error updating status for ID {id}: {e}")

# Close connections
cursor.close()
connection.close()

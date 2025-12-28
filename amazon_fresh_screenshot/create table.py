import pymysql
import db_config as db

# Connect to MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='actowiz',
    database='amazon_fresh_screenshot'
)

cursor = conn.cursor()


# SQL query to create table if it doesn't exist

def create_table():
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {db.pdp_data_table} (
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
      `On-site SKU Name` varchar(255) DEFAULT NULL,
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
      `amazon_approve_not_approve` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
      `hash_id` varchar(50) DEFAULT NULL,
      PRIMARY KEY (`Sr.No`),
      UNIQUE KEY `hash_id` (`hash_id`)
    )
    '''
    # Execute and commit
    cursor.execute(create_table_query)
    conn.commit()
    print("Table Created Successfully")


def pending_links():
    cursor.execute("SELECT COUNT(*) FROM pdp_link_table_21_06_2025 WHERE status = 'Done'")
    done_count = cursor.fetchone()[0]
    print(f"Done count: {done_count}")

    if done_count >= 800:
        update_query = "UPDATE pdp_link_table_21_06_2025 SET status = 'Pending' WHERE status = 'Done'"
        cursor.execute(update_query)
        conn.commit()
        print("Status updated to Pending All Links")


create_table()
pending_links()

# Close connection
cursor.close()
conn.close()

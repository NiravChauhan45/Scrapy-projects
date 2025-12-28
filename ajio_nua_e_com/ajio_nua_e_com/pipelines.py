from datetime import datetime
import pymysql
from ajio_nua_e_com.items import AjioNuaEComItem
from ajio_nua_e_com.config.database_config import ConfigDatabase
import ajio_nua_e_com.db_config as db


class AjioNuaEComPipeline:
    today_date = datetime.strftime(datetime.now(), '%d_%m_%Y')
    conn = pymysql.connect(
        database="ajio_nua_ecomm",
        user="root",
        host="localhost",
        password="actowiz"
    )
    cur = conn.cursor()

    def open_spider(self, spider):
        try:
            self.input_table = ConfigDatabase(table=f"{db.input_table}", database=f"{db.database_name}")
        except Exception as e:
            print(e)

        # Todo: Create table
        try:
            create_table = f"""
                CREATE TABLE `{db.input_table}` (
                      `Sr.No` int NOT NULL AUTO_INCREMENT,
                      `platform` varchar(20) DEFAULT NULL,
                      `datetime` varchar(100) DEFAULT NULL,
                      `keyword` varchar(100) DEFAULT NULL,
                      `pincode` varchar(10) DEFAULT NULL,
                      `product_id` varchar(100) DEFAULT NULL,
                      `product_url` varchar(255) DEFAULT NULL,
                      `product_name` varchar(255) DEFAULT NULL,
                      `Product_rank` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                      `mrp` varchar(10) DEFAULT NULL,
                      `selling_price` varchar(10) DEFAULT NULL,
                      `discount_percent` varchar(10) DEFAULT NULL,
                      `Product Image link` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                      `unique_key` varchar(150) DEFAULT NULL,
                      PRIMARY KEY (`Sr.No`),
                      UNIQUE KEY `product_id` (`unique_key`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
            """
            self.cur.execute(create_table)
            self.conn.commit()
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, AjioNuaEComItem):
                self.input_table.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

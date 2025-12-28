import pymysql
from big_basket_screenshot.config.database_config import ConfigDatabase
from big_basket_screenshot import db_config as db
from itemadapter import ItemAdapter
from big_basket_screenshot.items import BigBasketScreenshotItem
from loguru import logger


class BigBasketScreenshotPipeline:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database=db.database_name
    )

    def open_spider(self, spider):
        try:
            self.pdp_data_table = ConfigDatabase(table=db.pdp_data_table, database=db.database_name)
        except Exception as e:
            logger.error(e)

        # try:
        #     create_table = f"""
        #         CREATE TABLE `{db.pdp_data_table}` (
        #               `Sr.No` int NOT NULL AUTO_INCREMENT,
        #               `Portal Name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
        #               `Product Url` longtext,
        #               `Date (Crawler Date)` varchar(100) DEFAULT NULL,
        #               `Time (Crawler Time)` varchar(100) DEFAULT NULL,
        #               `City Name` varchar(255) DEFAULT NULL,
        #               `Pincode` varchar(100) DEFAULT NULL,
        #               `Brand` varchar(150) DEFAULT NULL,
        #               `Category` varchar(200) DEFAULT NULL,
        #               `SKU Packshot` varchar(200) DEFAULT NULL,
        #               `SKU Name` varchar(200) DEFAULT NULL,
        #               `On-site SKU Name` varchar(255) DEFAULT NULL,
        #               `Pack Size` varchar(200) DEFAULT NULL,
        #               `Single Pack` varchar(200) DEFAULT NULL,
        #               `Bundle Pack` varchar(200) DEFAULT NULL,
        #               `Per Gm Price (Unit Price)` varchar(20) DEFAULT NULL,
        #               `MRP` varchar(10) DEFAULT NULL,
        #               `Selling price` varchar(10) DEFAULT NULL,
        #               `Discount (%)` varchar(10) DEFAULT NULL,
        #               `Save Rs.` varchar(10) DEFAULT NULL,
        #               `Availability Status` varchar(30) DEFAULT NULL,
        #               `Quantity Caping` varchar(10) DEFAULT NULL,
        #               `Remarks` varchar(10) DEFAULT NULL,
        #               `Quantity` varchar(10) DEFAULT NULL,
        #               `Packaging of the product` varchar(40) DEFAULT NULL,
        #               `hash_id` varchar(50) DEFAULT NULL,
        #               PRIMARY KEY (`Sr.No`),
        #               UNIQUE KEY `hash_id` (`hash_id`)
        #             ) ENGINE=InnoDB AUTO_INCREMENT=468 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        #     """
        #     self.pdp_data_table.crsrSql.execute(create_table)
        # except Exception as error:
        #     logger.error(error)


    def process_item(self, item, spider):
        try:
            if isinstance(item, BigBasketScreenshotItem):
                self.pdp_data_table.insertItemToSql(item)
                mycursor = self.conn.cursor()
                sql = f"UPDATE {db.pdp_link_table} SET status = 'Finaly_Done' WHERE id = {item['Sr.No']}"
                mycursor.execute(sql)
                self.conn.commit()
                return item
        except Exception as e:
            print(e)

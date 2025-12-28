# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
# useful for handling different item types with a single interface
from nykaa.config.database_config import ConfigDatabase
from nykaa.items import NykaaPdpDataItem, Nykaa_N_PdpLinksItem
import nykaa.db_file as db


class NykaaPipeline:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database=f"{db.database_name}"
    )

    def open_spider(self, spider):
        try:
            self.pdp_links_table = ConfigDatabase(table=f"{db.pdp_links_table}", database=f"{db.database_name}")
            self.pdp_data_table = ConfigDatabase(table=f"{db.pdp_data_table}", database=f"{db.database_name}")
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE `{db.pdp_links_table}` (
                                  `id` int NOT NULL AUTO_INCREMENT,
                                  `brand` varchar(30) DEFAULT NULL,
                                  `product_id` varchar(30) DEFAULT NULL,
                                  `product_name` varchar(255) DEFAULT NULL,
                                  `product_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                                  `in_stock` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                                  `images_urls` longtext,
                                  `mrp` varchar(10) DEFAULT NULL,
                                  `price` varchar(10) DEFAULT NULL,
                                  `discount` varchar(10) DEFAULT NULL,
                                  `size_chart` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                                  `colour` varchar(200) DEFAULT NULL,
                                  `tags` varchar(100) DEFAULT NULL,
                                  `hash_id` varchar(100) DEFAULT NULL,
                                  `status` varchar(10) DEFAULT 'Pending',
                                  PRIMARY KEY (`id`),
                                  UNIQUE KEY `hash_id` (`hash_id`)
                                );
                            """
            self.pdp_links_table.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""
                CREATE TABLE `{db.pdp_data_table}` (
                  `Sr.No` int NOT NULL AUTO_INCREMENT,
                  `Category` varchar(30) DEFAULT NULL,
                  `Sub Category` varchar(30) DEFAULT NULL,
                  `Brand` varchar(30) DEFAULT NULL,
                  `Url` varchar(255) DEFAULT NULL,
                  `Product name` varchar(200) DEFAULT NULL,
                  `Image url` text,
                  `Star` varchar(10) DEFAULT NULL,
                  `Rating` varchar(10) DEFAULT NULL,
                  `Price` varchar(15) DEFAULT NULL,
                  `Discounted price` varchar(15) DEFAULT NULL,
                  `Color` varchar(30) DEFAULT NULL,
                  `Size` varchar(255) DEFAULT NULL,
                  `Fabric` varchar(30) DEFAULT NULL,
                  `Occasion` varchar(30) DEFAULT NULL,
                  `Neckline` varchar(30) DEFAULT NULL,
                  `Type of Work` varchar(35) DEFAULT NULL,
                  `Leg Style` varchar(35) DEFAULT NULL,
                  `Sets Subcategory` varchar(35) DEFAULT NULL,
                  `Sleeve Style` varchar(35) DEFAULT NULL,
                  `Pattern` varchar(40) DEFAULT NULL,
                  `Pack Size` varchar(50) DEFAULT NULL,
                  `Fit` varchar(25) DEFAULT NULL,
                  `Closure` varchar(30) DEFAULT NULL,
                  `Salwar Suits & Sets Subcategory` varchar(25) DEFAULT NULL,
                  `Rise Style` varchar(30) DEFAULT NULL,
                  `Care instructions` varchar(70) DEFAULT NULL,
                  `Pack contains` varchar(100) DEFAULT NULL,
                  `Description` text,
                  `Offer` json DEFAULT NULL,
                  `Promotion tag` varchar(200) DEFAULT NULL,
                  `hash_id` varchar(200) DEFAULT NULL,
                  `pagesave_id` varchar(100) DEFAULT NULL,
                  PRIMARY KEY (`Sr.No`),
                  UNIQUE KEY `hash_id` (`hash_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                """
            self.pdp_data_table.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, Nykaa_N_PdpLinksItem):
                self.pdp_links_table.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, NykaaPdpDataItem):
                self.pdp_data_table.insertItemToSql(item)
                mycursor = self.conn.cursor()
                sql = f"UPDATE {db.pdp_links_table} SET status = 'Done' WHERE hash_id = {item['pagesave_id']}"
                mycursor.execute(sql)
                self.conn.commit()
                return item
        except Exception as e:
            print(e)

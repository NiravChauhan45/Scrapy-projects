# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import mysql.connector

from nykaa_fashion.config.database_config import ConfigDatabase
from nykaa_fashion.items import NykaaFashionItem, NykaaPdpLinksItem, NykaaCategoryItem, NykaaCatItem, NykaaCatItemBrandId
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NykaaFashionPipeline:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="nykaa_fashion"
    )

    def open_spider(self, spider):
        today_date = datetime.now().strftime("%d_%m_%Y")
        try:
            self.ob = ConfigDatabase(table="category_links", database="nykaa_fashion")
            self.ob1 = ConfigDatabase(table="pdp_links", database="nykaa_fashion")
            self.ob2 = ConfigDatabase(table="pdp_data", database="nykaa_fashion")
            self.ob3 = ConfigDatabase(table="cat_links", database="nykaa_fashion")
            self.ob4 = ConfigDatabase(table="new_category_links_with_brand_id", database="nykaa_fashion")
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE `{self.ob.table}` (
                              `id` int NOT NULL AUTO_INCREMENT,
                              `main_category_name` varchar(200) DEFAULT NULL,
                              `category_name` varchar(200) DEFAULT NULL,
                              `sub_category_name` varchar(255) DEFAULT NULL,
                              `sub_category_url` varchar(255) DEFAULT NULL,
                              `hash_id` varchar(40) DEFAULT NULL,
                              `status` varchar(20) DEFAULT 'Pending',
                              PRIMARY KEY (`id`),
                              UNIQUE KEY `hash_id` (`hash_id`)
                            )"""
            self.ob.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE `{self.ob1.table}` (
                              `id` int NOT NULL AUTO_INCREMENT,
                              `main_category_name` varchar(30) DEFAULT NULL,
                              `category_name` varchar(30) DEFAULT NULL,
                              `sub_category_name` varchar(30) DEFAULT NULL,
                              `sub_category_id` varchar(30) DEFAULT NULL,
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
                              `sku` varchar(100) DEFAULT NULL,
                              `image_url` varchar(200) DEFAULT NULL,
                              `title` varchar(150) DEFAULT NULL,
                              `brand` varchar(255) DEFAULT NULL,
                              `hash_id` varchar(100) DEFAULT NULL,
                              `status` varchar(10) DEFAULT 'Pending',
                              PRIMARY KEY (`id`),
                              UNIQUE KEY `hash_id` (`hash_id`)
                            ) ENGINE=InnoDB AUTO_INCREMENT=17199 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                            """
            self.ob1.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE `{self.ob2.table}` (
                                  `S.No.` int NOT NULL AUTO_INCREMENT,
                                  `Website` varchar(25) DEFAULT 'Nykaa Fashion',
                                  `PID` varchar(30) DEFAULT NULL,
                                  `Name` varchar(255) DEFAULT NULL,
                                  `Short Description` text DEFAULT NULL,
                                  `Description` text DEFAULT NULL,
                                  `Category` varchar(255) DEFAULT NULL,
                                  `Image URL` varchar(255) DEFAULT NULL,
                                  `Price` varchar(10) DEFAULT NULL,
                                  `Price Currency` varchar(10) DEFAULT NULL,
                                  `Sale Price` varchar(10) DEFAULT NULL,
                                  `Final Price` varchar(10) DEFAULT NULL,
                                  `Discount` varchar(10) DEFAULT NULL,
                                  `IsOnSale` varchar(10) DEFAULT NULL,
                                  `IsInStock` varchar(10) DEFAULT NULL,
                                  `Keywords` varchar(10) DEFAULT 'N/A',
                                  `Brand` varchar(255) DEFAULT NULL,
                                  `Manufacturer` text DEFAULT NULL,
                                  `MPN` varchar(255) DEFAULT NULL,
                                  `UPC or EAN` varchar(255) DEFAULT NULL,
                                  `SKU` varchar(255) DEFAULT NULL,
                                  `Colour` varchar(50) DEFAULT NULL,
                                  `Gender` varchar(50) DEFAULT NULL,
                                  `Size` varchar(255) DEFAULT NULL,
                                  `Variant Price` varchar(255) DEFAULT NULL,
                                  `Alternate Image URLs` longtext,
                                  `Link URL` varchar(255) DEFAULT NULL,
                                  `Num Ratings` varchar(10) DEFAULT NULL,
                                  `Average Ratings` varchar(10) DEFAULT NULL,
                                  `hash_id` varchar(10) DEFAULT NULL,
                                  PRIMARY KEY (`S.No.`),
                                  UNIQUE KEY `Product_id` (`PID`)
                                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
            self.ob2.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""
                CREATE TABLE `{self.ob3.table}` (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `main_category_name` varchar(255) DEFAULT NULL,
                  `category_id` varchar(20) DEFAULT NULL,
                  `category_name` varchar(255) DEFAULT NULL,
                  `sub_category_id` varchar(200) DEFAULT NULL,
                  `sub_category_name` varchar(255) DEFAULT NULL,
                  `sub_category_url` varchar(255) DEFAULT NULL,
                  `sub_category_product_count` varchar(20) DEFAULT NULL,
                  `hash_id` varchar(20) DEFAULT NULL,
                  `status` varchar(20) DEFAULT 'Pending',
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `hash_id` (`hash_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                """
            self.ob3.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, NykaaCategoryItem):
                self.ob.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, NykaaPdpLinksItem):
                self.ob1.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, NykaaFashionItem):
                self.ob2.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, NykaaCatItem):
                self.ob3.insertItemToSql(item)
                mycursor = self.conn.cursor()
                sql = f"UPDATE {self.ob1.table} SET status = 'Done' WHERE hash_id = {item['hash_id']}"
                mycursor.execute(sql)
                self.conn.commit()
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, NykaaCatItemBrandId):
                self.ob4.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)
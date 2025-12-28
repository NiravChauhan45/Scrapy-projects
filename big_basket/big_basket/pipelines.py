# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from big_basket.config.database_config import ConfigDatabase
from big_basket.items import BigbasketLinksItem, BigbasketPdpDataItem


class BigBasketPipeline:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="big_basket"
    )
    def open_spider(self, spider):
        try:
            self.ob1 = ConfigDatabase(table="pdp_links", database="big_basket")
            self.ob2 = ConfigDatabase(table="pdp_data", database="big_basket")
        except Exception as e:
            print(e)
        try:
            create_table = f"""CREATE TABLE `{self.ob1.table}` (
                              `id` int NOT NULL AUTO_INCREMENT,
                              `sitemap_url` varchar(255) DEFAULT NULL,
                              `product_url` varchar(255) DEFAULT NULL,
                              `status` varchar(10) DEFAULT 'Pending',
                              PRIMARY KEY (`id`)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                            """
            self.ob1.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE `big_basket`.`{self.ob2.table}` (  
                                  `id` INT NOT NULL AUTO_INCREMENT,
                                  `Product Code` VARCHAR(100),
                                  `Product Name` VARCHAR(255),
                                  `Attributes` VARCHAR(250),
                                  `MRP` VARCHAR(10),
                                  `Discount` VARCHAR(10),
                                  `Availability` VARCHAR(10),
                                  `Category` VARCHAR(255),
                                  `Sub Category` VARCHAR(255),
                                  `Other Category` VARCHAR(255),
                                  `Selling Price` VARCHAR(10),
                                  `Image URL` TEXT,
                                  `About Product` TEXT,		/* Length must be specified for varchar data type */
                                  `Other Info` TEXT,
                                  `Description JSON` JSON,
                                  `Product URL` VARCHAR(250),
                                  UNIQUE KEY `Product URL` (`Product URL`),
                                  PRIMARY KEY (`id`) 
                                );"""
            self.ob2.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, BigbasketLinksItem):
                self.ob1.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, BigbasketPdpDataItem):
                self.ob2.insertItemToSql(item)
                mycursor = self.conn.cursor()
                sql = f"UPDATE {self.ob1.table} SET status = 'Done' WHERE id = {item['id']}"
                mycursor.execute(sql)
                self.conn.commit()
                return item
        except Exception as e:
            print(e)

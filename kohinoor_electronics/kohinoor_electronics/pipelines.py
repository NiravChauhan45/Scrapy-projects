# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import mysql.connector
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kohinoor_electronics.config.database_config import ConfigDatabase
from kohinoor_electronics.items import extract_product_url_item, product_data_item


class KohinoorElectronicsPipeline:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="kohinoor_electronics"
    )

    def open_spider(self, spider):
        today_date = datetime.strftime(datetime.now(), '%d_%m_%Y')

        try:
            self.ob1 = ConfigDatabase(table=f'extract_product_urls', database='kohinoor_electronics')
            self.ob2 = ConfigDatabase(table=f'product_data', database='kohinoor_electronics')
        except Exception as e:
            spider.logger.info(e)

        try:
            create_table = f"""CREATE TABLE IF NOT EXISTS `{self.ob1.table}` (`id` INT NOT NULL AUTO_INCREMENT,
                                                                              `main_category_name` VARCHAR(255),
                                                                              `product_id` VARCHAR(100),
                                                                              `product_name` VARCHAR(250),
                                                                              `product_url` VARCHAR(255),
                                                                              `status` VARCHAR(100) DEFAULT 'Pending',
                                                                               PRIMARY KEY (`id`) ,
                                                                               UNIQUE INDEX (`product_id`));"""
            self.ob1.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE IF NOT EXISTS `{self.ob2.table}` (`id` int NOT NULL AUTO_INCREMENT,
                                                                              `product_id` varchar(50) DEFAULT NULL,
                                                                              `catalog_name` varchar(255) DEFAULT NULL,
                                                                              `catalog_id` varchar(50) DEFAULT NULL,
                                                                              `source` varchar(50) DEFAULT 'Kohinoor',
                                                                              `scraped_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
                                                                              `product_name` varchar(255) DEFAULT NULL,
                                                                              `image_url` varchar(255) DEFAULT NULL,
                                                                              `category_hierarchy` json DEFAULT NULL,
                                                                              `product_price` varchar(50) DEFAULT NULL,
                                                                              `arrival_date` varchar(50) DEFAULT NULL,
                                                                              `shipping_charges` varchar(200) DEFAULT NULL,
                                                                              `is_sold_out` varchar(50) DEFAULT NULL,
                                                                              `discount` varchar(50) DEFAULT NULL,
                                                                              `mrp` varchar(50) DEFAULT NULL,
                                                                              `page_url` varchar(255) DEFAULT NULL,
                                                                              `product_url` varchar(255) DEFAULT NULL,
                                                                              `number_of_ratings` varchar(50) DEFAULT NULL,
                                                                              `avg_rating` varchar(50) DEFAULT NULL,
                                                                              `position` varchar(200) DEFAULT NULL,
                                                                              `country_code` varchar(50) DEFAULT 'IN',
                                                                              `others` json DEFAULT NULL,
                                                                              `page_save_id` varchar(100) DEFAULT NULL UNIQUE,
                                                                               PRIMARY KEY (`id`));"""
            self.ob2.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, extract_product_url_item):
                self.ob1.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, product_data_item):
                cur = self.conn.cursor()
                cur.execute(
                    f"""insert into product_data (product_id, catalog_name, catalog_id, source, product_name, image_url, category_hierarchy, product_price,arrival_date, shipping_charges, is_sold_out, discount, mrp, page_url, product_url, number_of_ratings, avg_rating, position, country_code, others, page_save_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (item['product_id'], item['catalog_name'], item['catalog_id'], item['source'],
                     item['product_name'], item['image_url'], item['category_hierarchy'], item['product_price'],
                     item['arrival_date'], item['shipping_charges'], item['is_sold_out'], item['discount'], item['mrp'],
                     item['page_url'],
                     item['product_url'], item['number_of_ratings'], item['avg_rating'], item['position'],
                     item['country_code'], item['others'], item['page_save_id']))
                self.conn.commit()
                return item
                print(f"inserted data....")

        except Exception as e:
            print(e)

    # self.ob2.insertItemToSql(item)

# except Exception as e:
#     print(e)

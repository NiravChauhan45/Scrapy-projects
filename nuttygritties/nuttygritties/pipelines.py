# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from nuttygritties.config.database_config import ConfigDatabase
from nuttygritties.items import NuttygrittiesItem, NuttygrittiesUrlItem, NuttygrittiesNewProductItem


class NuttygrittiesPipeline:
    def open_spider(self, spider):
        today_date = datetime.strftime(datetime.now(), '%d_%m_%Y')

        try:
            self.ob1 = ConfigDatabase(table=f'product_data', database='nuttygritties')
            self.ob2 = ConfigDatabase(table=f'product_url', database='nuttygritties')
            self.ob3 = ConfigDatabase(table=f'product_data_{today_date}', database='nuttygritties')
        except Exception as e:
            spider.logger.info(e)

        try:
            create_table = f"""CREATE TABLE `{self.ob1.table}` (`id` int NOT NULL AUTO_INCREMENT,
                                                                `platform` varchar(255) DEFAULT NULL,
                                                                `date` varchar(255) DEFAULT NULL,
                                                                `SKU` varchar(50) DEFAULT NULL,
                                                                `Brand` varchar(250) DEFAULT NULL,
                                                                `Pincode` varchar(50) DEFAULT NULL,
                                                                `Product_name` varchar(200) DEFAULT NULL,
                                                                `Product_id` varchar(100) DEFAULT NULL,
                                                                `Product_url` varchar(255) DEFAULT NULL,
                                                                `Mrp` varchar(255) DEFAULT NULL,
                                                                `Selling_price` varchar(50) DEFAULT NULL,
                                                                `Unit_price` varchar(50) DEFAULT NULL,
                                                                `Discount_percentage` varchar(50) DEFAULT NULL,
                                                                `Discount_amount` varchar(50) DEFAULT NULL,
                                                                `Stock` varchar(10) DEFAULT NULL,
                                                                PRIMARY KEY (`id`),
                                                                UNIQUE KEY `Product_url` (`Product_url`))"""
            self.ob1.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE `{self.ob3.table}` (`id` int NOT NULL AUTO_INCREMENT,
                                                                `platform` varchar(255) DEFAULT NULL,
                                                                `category_name` varchar(255) DEFAULT NULL,
                                                                `date` varchar(255) DEFAULT NULL,
                                                                `SKU` varchar(50) DEFAULT NULL,
                                                                `Brand` varchar(250) DEFAULT NULL,
                                                                `Pincode` varchar(50) DEFAULT NULL,
                                                                `Product_name` varchar(200) DEFAULT NULL,
                                                                `Product_id` varchar(100) DEFAULT NULL,
                                                                `Product_url` varchar(255) DEFAULT NULL,
                                                                `Mrp` varchar(255) DEFAULT NULL,
                                                                `Selling_price` varchar(50) DEFAULT NULL,
                                                                `Unit_price` varchar(50) DEFAULT NULL,
                                                                `Discount_percentage` varchar(50) DEFAULT NULL,
                                                                `Discount_amount` varchar(50) DEFAULT NULL,
                                                                `Stock` varchar(10) DEFAULT NULL,
                                                                PRIMARY KEY (`id`),
                                                                UNIQUE KEY `Product_url` (`Product_url`))"""
            self.ob3.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE `{self.ob2.table}` (`id` INT NOT NULL AUTO_INCREMENT,
                                                                `urls` VARCHAR(255),
                                                                `hash_key` VARCHAR(255) UNIQUE,
                                                                `status` VARCHAR(255) DEFAULT 'Pending',
                                                                 PRIMARY KEY (`id`))"""
            self.ob2.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, NuttygrittiesItem):
                self.ob1.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, NuttygrittiesUrlItem):
                self.ob2.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, NuttygrittiesNewProductItem):
                self.ob3.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

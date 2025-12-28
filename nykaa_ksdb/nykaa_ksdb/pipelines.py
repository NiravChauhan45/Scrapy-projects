# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from nykaa_ksdb.config.database_config import ConfigDatabase
from nykaa_ksdb.items import NykaaKsdbItem
class NykaaKsdbPipeline:

    def open_spider(self, spider):
        try:
            self.pdp_data_table = ConfigDatabase(table=f"pdp_data", database=f"nykaa_ksdb")
        except Exception as e:
            print(e)

        try:
            create_table = """
                CREATE TABLE `pdp_data` (
                      `Id` int NOT NULL AUTO_INCREMENT,
                      `product_id` varchar(40) NOT NULL,
                      `catalog_name` varchar(500) NOT NULL,
                      `catalog_id` varchar(40) NOT NULL,
                      `source` varchar(40) DEFAULT 'amazon',
                      `scraped_date` datetime DEFAULT CURRENT_TIMESTAMP,
                      `product_name` varchar(500) DEFAULT 'N/A',
                      `image_url` varchar(500) DEFAULT 'N/A',
                      `category_hierarchy` json DEFAULT NULL,
                      `product_price` decimal(9,2) DEFAULT NULL,
                      `arrival_date` varchar(40) DEFAULT 'N/A',
                      `shipping_charges` varchar(140) DEFAULT NULL,
                      `is_sold_out` varchar(40) DEFAULT 'false',
                      `discount` varchar(40) DEFAULT 'N/A',
                      `mrp` decimal(9,2) DEFAULT NULL,
                      `page_url` varchar(300) DEFAULT 'N/A',
                      `product_url` varchar(500) NOT NULL,
                      `number_of_ratings` int DEFAULT NULL,
                      `review` float DEFAULT NULL,
                      `position` varchar(5) DEFAULT 'N/A',
                      `country_code` varchar(2) DEFAULT 'IN',
                      `others` json DEFAULT NULL,
                      `is_login` int DEFAULT '0',
                      `is_zip` int DEFAULT '0',
                      `zip_code` int DEFAULT '0',
                      `department` varchar(50) DEFAULT 'old',
                      `shipping_charges_json` json DEFAULT (json_object()),
                      `product_price_json` json DEFAULT (json_object()),
                      `mrp_json` json DEFAULT (json_object()),
                      `discount_json` json DEFAULT (json_object()),
                      PRIMARY KEY (`Id`)
                    ) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
            """
            self.pdp_data_table.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, NykaaKsdbItem):
                self.pdp_data_table.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

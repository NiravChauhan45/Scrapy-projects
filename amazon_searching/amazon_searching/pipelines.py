# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from amazon_searching.config.database_config import ConfigDatabase
from amazon_searching.items import AmazonSearchingItem, AmazonSearchingPdpItem, AmazonBeautyCareItem


class AmazonSearchingPipeline:
    def open_spider(self, spider):
        try:
            self.pdp_links_table = ConfigDatabase(table=f"new_category_table", database=f"amazon_searching")
            self.pdp_data_table = ConfigDatabase(table=f"pdp_data", database=f"amazon_searching")
            self.beauty_personal_care_cat_links = ConfigDatabase(table=f"beauty_personal_care_cat_links",
                                                                 database=f"amazon_searching")
            self.health_care = ConfigDatabase(table=f"health_care",
                                                                 database=f"amazon_searching")
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE `{self.pdp_links_table.table}` (
                                  `id` int NOT NULL AUTO_INCREMENT,
                                  `main_category_name` varchar(255) DEFAULT NULL,
                                  `main_category_url` varchar(255) DEFAULT NULL,
                                  `category_name` varchar(255) DEFAULT NULL,
                                  `category_url` varchar(255) DEFAULT NULL,
                                  `sub_category_name` varchar(255) DEFAULT NULL,
                                  `sub_category_url` varchar(255) DEFAULT NULL,
                                  `hash_id` varchar(50) DEFAULT NULL,
                                  PRIMARY KEY (`id`),
                                  UNIQUE KEY `hash_id` (`hash_id`)
                                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
            self.pdp_links_table.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE `{self.health_care.table}` (
                                  `id` int NOT NULL AUTO_INCREMENT,
                                  `main_category_name` varchar(255) DEFAULT NULL,
                                  `main_category_url` varchar(500) DEFAULT NULL,
                                  `category_name` varchar(255) DEFAULT NULL,
                                  `category_url` varchar(500) DEFAULT NULL,
                                  `sub_category_name` varchar(260) DEFAULT NULL,
                                  `sub_category_url` varchar(500) DEFAULT NULL,
                                  `child_category_name` varchar(250) DEFAULT NULL,
                                  `child_category_url` varchar(500) DEFAULT NULL,
                                  `breadcrumbs` json DEFAULT NULL,
                                  `product_count` varchar(10) DEFAULT NULL,
                                  `hash_id` varchar(50) DEFAULT NULL,
                                  PRIMARY KEY (`id`),
                                  UNIQUE KEY `hash_id` (`hash_id`)
                                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
            self.health_care.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, AmazonSearchingItem):
                self.pdp_links_table.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, AmazonSearchingPdpItem):
                self.pdp_data_table.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, AmazonBeautyCareItem):
                self.health_care.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

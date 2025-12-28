from loguru import logger
from amazon_seller.config.database_config import ConfigDatabase
from amazon_seller.items import AmazonSellerItem, GetVariationIdItem
import amazon_seller.config.db_config as db_config


class AmazonSellerPipeline:

    def __init__(self):
        self.product_link_table = ConfigDatabase(table=db_config.product_link_table,
                                                 database=db_config.database_name)
        self.variation_id_table = ConfigDatabase(table=db_config.variation_id_table,
                                                 database=db_config.database_name)

    def open_spider(self, spider):
        # Todo: Create Table If Not Exists
        try:
            create_table = f"""
                CREATE TABLE IF NOT EXISTS `{db_config.product_link_table}` (
                      `id` int NOT NULL AUTO_INCREMENT,
                      `item_type` varchar(200) DEFAULT NULL,
                      `product_id` varchar(100) DEFAULT NULL,
                      `product_url` varchar(200) DEFAULT NULL,
                      `status` varchar(100) DEFAULT 'Pending',
                      PRIMARY KEY (`id`),
                      UNIQUE KEY `UNIQUE` (`product_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
            """
            self.product_link_table.crsrSql.execute(create_table)
        except Exception as error:
            logger.error("Error In Open Spider: ", error)

        try:
            create_table = f"""
                CREATE TABLE IF NOT EXISTS `{db_config.variation_id_table}` (
                      `id` int NOT NULL AUTO_INCREMENT,
                      `item_type` varchar(200) DEFAULT NULL,
                      `product_url` varchar(255) DEFAULT NULL,
                      `parent_pid` varchar(50) DEFAULT NULL,
                      `child_pid` varchar(50) DEFAULT NULL,
                      `sr_nos_1` varchar(10) DEFAULT NULL,
                      `sr_nos_2` varchar(10) DEFAULT NULL,
                      `unique_key` varchar(50) DEFAULT NULL,
                      `status` varchar(10) DEFAULT 'Pending',
                      PRIMARY KEY (`id`),
                      UNIQUE KEY `unique_key` (`unique_key`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
            """
            self.variation_id_table.crsrSql.execute(create_table)
        except Exception as error:
            logger.error("Error In Open Spider: ", error)

    def process_item(self, item, spider):
        try:
            if isinstance(item, AmazonSellerItem):
                self.product_link_table.insertItemToSql(item)
                logger.success(f"{item['product_id']} is successfully inserted..")
                return item
        except Exception as error:
            logger.error("Error In Process AmazonSellerItem: ", error)

        try:
            if isinstance(item, GetVariationIdItem):
                self.variation_id_table.insertItemToSql(item)
                logger.success(f"{item['parent_pid']} is successfully inserted..")
                return item
        except Exception as error:
            logger.error("Error In Process GetVariationIdItem: ", error)

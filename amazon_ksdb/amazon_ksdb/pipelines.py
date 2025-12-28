from amazon_ksdb.items import AmazonKsdbInputItem
from amazon_ksdb.config.database_config import ConfigDatabase
import amazon_ksdb.config.db_config as db


class AmazonKsdbPipeline:
    def open_spider(self, spider):
        try:
            self.input_table = ConfigDatabase(table=f"{db.input_table}", database=f"{db.database_name}")
        except Exception as e:
            print(e)

        # Todo: Cretae Input_table
        try:
            create_table = f"""
                CREATE TABLE `{db.input_table}` (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `product_id` varchar(100) DEFAULT NULL,
                  `product_url` varchar(255) DEFAULT NULL,
                  `status` varchar(10) DEFAULT 'Pending',
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `UNique` (`product_url`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
            """
            self.input_table.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, AmazonKsdbInputItem):
                self.input_table.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

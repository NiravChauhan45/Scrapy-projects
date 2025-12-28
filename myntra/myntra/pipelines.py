# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import myntra.db_config as db
from myntra.config.database_config import ConfigDatabase
from myntra.items import MyntraItem


class MyntraPipeline:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database=db.database_name
    )

    def open_spider(self, spider):
        try:
            self.pdp_links_table = ConfigDatabase(table=f"{db.pdp_links_table}", database=f"{db.database_name}")
        except Exception as e:
            print(e)

        # Todo: Create Table If not exists
        try:
            create_table = f"""CREATE TABLE IF NOT EXISTS `{db.pdp_links_table}` (
                                      `id` int NOT NULL AUTO_INCREMENT,
                                      `keyword` varchar(200) DEFAULT NULL,
                                      `product_id` varchar(200) DEFAULT NULL,
                                      `product_url` text,
                                      `status` varchar(20) DEFAULT 'Pending',
                                      PRIMARY KEY (`id`),
                                      UNIQUE KEY `UNIQUE` (`product_id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                                    """
            self.pdp_links_table.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, MyntraItem):
                self.pdp_links_table.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from amazon_momcozy.config.database_config import ConfigDatabase
from amazon_momcozy.items import AmazonMomcozyItem


class AmazonMomcozyPipeline:
    def open_spider(self, spider):
        try:
            self.category_table = ConfigDatabase( database=f"amazon_momcozy",table=f"category_links")
        except Exception as e:
            print("error: ",e)
        try:
            create_table = f"""CREATE TABLE `{self.category_table.table}` (
                                  `id` int NOT NULL AUTO_INCREMENT,
                                  `category_name` varchar(200) DEFAULT NULL,
                                  `category_url` varchar(250) DEFAULT NULL,
                                  `status` varchar(10) DEFAULT 'Pending',
                                  PRIMARY KEY (`id`),
                                  UNIQUE KEY `category_url` (`category_url`)
                                ) """
            self.category_table.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, AmazonMomcozyItem):
                self.category_table.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

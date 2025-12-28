# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from amf_france.config.database_config import ConfigDatabase
from amf_france.items import AmfFranceItem


class AmfFrancePipeline:
    def open_spider(self, spider):
        today_date = datetime.strftime(datetime.now(), '%d_%m_%Y')

        try:
            self.ob1 = ConfigDatabase(table='get_urls', database='amf_france')
        except Exception as e:
            spider.logger.info(e)

        try:
            create_table = f"""CREATE TABLE IF NOT EXISTS `{self.ob1.table}`(
                                    `id` int NOT NULL AUTO_INCREMENT,
                                    `theme` varchar(200) DEFAULT NULL,
                                    `title` varchar(255) DEFAULT NULL,
                                    `url` varchar(255) DEFAULT NULL UNIQUE,
                                    `status` varchar(100) DEFAULT 'pending',
                                     PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                                    """
            self.ob1.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, AmfFranceItem):
                self.ob1.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

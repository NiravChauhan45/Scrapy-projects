# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from chatime_canada.config.database_config import ConfigDatabase

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from chatime_canada.items import ChatimeCanadaItem, ChatimeCanadaStoreLocationItem


class ChatimeCanadaPipeline:
    def open_spider(self, spider):
        today_date = datetime.strftime(datetime.now(), '%d_%m_%Y')

        try:
            self.ob1 = ConfigDatabase(table=f'find_locations', database='chatime_canada')
            self.ob2 = ConfigDatabase(table=f'final_locations_data', database='chatime_canada')
        except Exception as e:
            spider.logger.info(e)

        try:
            create_table = f"""CREATE TABLE IF NOT EXISTS `{self.ob1.table}` (`id` INT NOT NULL AUTO_INCREMENT,
                                                                `store_no` VARCHAR(250),
                                                                `store_name` VARCHAR(250),
                                                                `store_url` VARCHAR(250),
                                                                `latitude` VARCHAR(250),
                                                                `longitude` VARCHAR(250),
                                                                `street` VARCHAR(250),
                                                                `zipcode` VARCHAR(250),
                                                                `city_name` VARCHAR(255),
                                                                `country_code` VARCHAR(255),
                                                                `phone_number` VARCHAR(255),
                                                                `hash_key` VARCHAR(255),
                                                                `status` VARCHAR(255) DEFAULT 'Pending',
                                                                PRIMARY KEY (`id`) ,
                                                                UNIQUE INDEX (`hash_key`));"""
            self.ob1.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE IF NOT EXISTS `{self.ob2.table}` (`Id` int NOT NULL AUTO_INCREMENT,
                                                                              `Store_No` varchar(250) DEFAULT NULL,
                                                                              `Name` varchar(250) DEFAULT NULL,
                                                                              `Latitude` varchar(255) DEFAULT NULL,
                                                                              `Longitude` varchar(250) DEFAULT NULL,
                                                                              `Street` varchar(150) DEFAULT NULL,
                                                                              `City` varchar(50) DEFAULT NULL,
                                                                              `Province` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'ON',
                                                                              `Zip_Code` varchar(50) DEFAULT NULL,
                                                                              `Phone` varchar(50) DEFAULT NULL,
                                                                              `Open_Hours` text,
                                                                              `URL` varchar(255) DEFAULT NULL,
                                                                              `Provider` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'Chatime',
                                                                              `Updated_date` varchar(100) DEFAULT NULL,
                                                                              `Country` varchar(250) DEFAULT 'Canada',
                                                                              `Status` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'Open',
                                                                              `Direction_URL` varchar(255) DEFAULT NULL,
                                                                              PRIMARY KEY (`id`)
                                                                            );"""
            self.ob2.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, ChatimeCanadaItem):
                self.ob1.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, ChatimeCanadaStoreLocationItem):
                self.ob2.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

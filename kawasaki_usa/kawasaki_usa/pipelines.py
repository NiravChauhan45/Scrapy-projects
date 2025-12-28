# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kawasaki_usa.config.database_config import ConfigDatabase
from kawasaki_usa.items import KawasakiUsaItem, NewKawasakiUsaItem


class KawasakiUsaPipeline:
    def open_spider(self, spider):
        today_date = datetime.strftime(datetime.now(), '%d_%m_%Y')

        try:
            # self.ob1 = ConfigDatabase(table=f'location_data', database='kawasaki_usa')
            self.ob2 = ConfigDatabase(table=f'kawasaki_locations_data', database='kawasaki_usa')
        except Exception as e:
            spider.logger.info(e)

        # try:
        #     create_table = f"""CREATE TABLE `{self.ob1.table}` (`id` INT NOT NULL AUTO_INCREMENT,
        #                                                         `Store_no` VARCHAR(50),
        #                                                         `Name` VARCHAR(255),
        #                                                         `Latitude` VARCHAR(50),
        #                                                         `Longitude` VARCHAR(50),
        #                                                         `Street` VARCHAR(200),
        #                                                         `City` VARCHAR(100),
        #                                                         `State` VARCHAR(50),
        #                                                         `Zip_code` VARCHAR(50),
        #                                                         `County` VARCHAR(250),
        #                                                         `Phone` VARCHAR(100),
        #                                                         `Url` VARCHAR(255),
        #                                                         `Provider` VARCHAR(255) DEFAULT 'Kawasaki',
        #                                                         `Updated_Date` VARCHAR(255),
        #                                                         `Status` VARCHAR(50) DEFAULT 'Open',
        #                                                         `Direction` VARCHAR(255),
        #                                                         `NAICS 1` VARCHAR(255) DEFAULT '441227 - Motorcycle, ATV, and All Other Motor Vehicle Dealers',
        #                                                         `NAICS 2` VARCHAR(255) DEFAULT '423120 - Motor Vehicle Supplies and New Parts Merchant Wholesalers',
        #                                                         `SIC 1` VARCHAR(255) DEFAULT '55710000 - Motorcycle dealers',
        #                                                         `SIC 2` VARCHAR(255) DEFAULT '55710000 - Motorcycle dealers',
        #                                                         `Stock Ticker` VARCHAR(250) DEFAULT 'KWHIY:OTCMKTS',
        #                                                         `hash_key` VARCHAR(255) UNIQUE,
        #                                                          PRIMARY KEY (`id`));"""
        #     self.ob1.crsrSql.execute(create_table)
        # except Exception as e:
        #     print(e)

        try:
            create_table = f"""CREATE TABLE IF NOT EXISTS `{self.ob2.table}` (`id` INT NOT NULL AUTO_INCREMENT,
                                                                `Store_no` VARCHAR(50),
                                                                `Name` VARCHAR(255),
                                                                `Latitude` VARCHAR(50),
                                                                `Longitude` VARCHAR(50),
                                                                `Street` VARCHAR(200),
                                                                `City` VARCHAR(100),
                                                                `State` VARCHAR(50),
                                                                `Zip_code` VARCHAR(50),
                                                                `County` VARCHAR(250),
                                                                `Phone` VARCHAR(100),
                                                                `Url` VARCHAR(255),
                                                                `Provider` VARCHAR(255) DEFAULT 'Kawasaki',
                                                                `Updated_Date` VARCHAR(255),
                                                                `Status` VARCHAR(50) DEFAULT 'Open',
                                                                `Direction_URL` VARCHAR(255),
                                                                `NAICS 1` VARCHAR(255) DEFAULT '441227 - Motorcycle, ATV, and All Other Motor Vehicle Dealers',
                                                                `NAICS 2` VARCHAR(255) DEFAULT '423120 - Motor Vehicle Supplies and New Parts Merchant Wholesalers',
                                                                `SIC 1` VARCHAR(255) DEFAULT '55710000 - Motorcycle dealers',
                                                                `SIC 2` VARCHAR(255) DEFAULT '55710000 - Motorcycle dealers',
                                                                `Stock Ticker` VARCHAR(250) DEFAULT 'KWHIY:OTCMKTS',
                                                                `hash_key` VARCHAR(255) UNIQUE,
                                                                 PRIMARY KEY (`id`));"""
            self.ob2.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        # try:
        #     if isinstance(item, KawasakiUsaItem):
        #         self.ob1.insertItemToSql(item)
        #         return item
        # except Exception as e:
        #     print(e)

        try:
            if isinstance(item, NewKawasakiUsaItem):
                self.ob2.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

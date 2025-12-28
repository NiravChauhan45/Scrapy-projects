# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dmart.items import DmartItem, dmart_product_data
from dmart.config.database_config import ConfigDatabase


class DmartPipeline:
    def open_spider(self, spider):
        today_date = datetime.strftime(datetime.now(), '%Y%m%d')

        try:
            self.ob1 = ConfigDatabase(table=f'category', database='new_dmart')
            self.ob2 = ConfigDatabase(table=f'product_data', database='new_dmart')
        except Exception as e:
            spider.logger.info(e)

        try:
            create_table = f"""CREATE TABLE `{self.ob1.table}` (`id` INT NOT NULL AUTO_INCREMENT,
                                                                `city_name` VARCHAR(255),
                                                                `store_id` VARCHAR(50),
                                                                `main_category_name` VARCHAR(255),
                                                                `sub_category_name` VARCHAR(255),
                                                                `child_category_name` VARCHAR(255),
                                                                `child_category_slug` VARCHAR(255),
                                                                `child_category_url` VARCHAR(255),
                                                                `hash_key` VARCHAR(255),
                                                                `status` VARCHAR(50) DEFAULT 'Pending',
                                                                PRIMARY KEY (`id`) ,
                                                                INDEX (`hash_key`))"""
            self.ob1.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE `{self.ob2.table}` (`id` INT NOT NULL AUTO_INCREMENT,
                                                                `city_name` VARCHAR(255),
                                                                `Competitor` VARCHAR(50) DEFAULT 'Dmart',
                                                                `Pincode` VARCHAR(50),
                                                                `main_category_name` VARCHAR(255),
                                                                `sub_category_name` VARCHAR(255),
                                                                `child_category_name` VARCHAR(255),
                                                                `Product_ID` VARCHAR(255),
                                                                `sku_unique_id` VARCHAR(255),
                                                                `Instock` VARCHAR(50),
                                                                `Url` VARCHAR(255),
                                                                `Name` VARCHAR(255),
                                                                `new_hash_key` VARCHAR(255),
                                                                `page_save_id` VARCHAR(255),
                                                                PRIMARY KEY (`id`) ,
                                                                UNIQUE INDEX (`new_hash_key`)
                                                                )"""
            self.ob2.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, DmartItem):
                self.ob1.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, dmart_product_data):
                self.ob2.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

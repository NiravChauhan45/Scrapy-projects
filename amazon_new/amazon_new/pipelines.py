# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from amazon_new.items import AmazonPlItem, AmazonPdpItem
from amazon_new.config.database_config import ConfigDatabase


class AmazonNewPipeline:
    def __init__(self):
        today_date = datetime.strftime(datetime.now(), '%d_%m_%Y')

        try:
            self.ob1 = ConfigDatabase(table=f'pl_page_data', database='amazon_new')
            self.ob2 = ConfigDatabase(table=f'final_product_data', database='amazon_new')
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE IF NOT EXISTS `{self.ob1.table}` (`id` INT NOT NULL AUTO_INCREMENT,
                                                                              `product_name` VARCHAR(255),
                                                                              `product_url` LONGTEXT,
                                                                              `sponsored` TEXT(100),
                                                                              `badge` VARCHAR(150),
                                                                              `page_rank` VARCHAR(10),
                                                                              `srp_no` VARCHAR(10),
                                                                              `Price` varchar(20) DEFAULT NULL,
                                                                              `Price_per_unit` varchar(20) DEFAULT NULL,
                                                                              `hash_key` VARCHAR(50),
                                                                              `status` VARCHAR(10) DEFAULT 'Pending',
                                                                              PRIMARY KEY (`id`) ,
                                                                              UNIQUE INDEX (`hash_key`));"""
            self.ob1.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

        try:
            create_table = f"""CREATE TABLE IF NOT EXISTS `{self.ob2.table}` (`id` int NOT NULL AUTO_INCREMENT,
                                                                             `Primary_image` longtext DEFAULT NULL,
                                                                             `Product_title` text DEFAULT NULL,
                                                                             `Price` varchar(20) DEFAULT NULL,
                                                                             `Price_per_unit` varchar(20) DEFAULT NULL,
                                                                             `Price_discount` varchar(20) DEFAULT NULL,
                                                                             `Star_ratings` varchar(20) DEFAULT NULL,
                                                                             `No_of_reviews` varchar(20) DEFAULT NULL,
                                                                             `Page_rank` varchar(10) DEFAULT NULL,
                                                                             `SRP_no` varchar(200) DEFAULT NULL,
                                                                             `Brand_name` varchar(100) DEFAULT NULL,
                                                                             `Product_ASIN` varchar(100) DEFAULT NULL,
                                                                             `Badges` varchar(150) DEFAULT NULL,
                                                                             `Sponsored` varchar(100) DEFAULT NULL,
                                                                             `Breadcrumb_menu` text DEFAULT NULL,
                                                                             `Brand` varchar(100) DEFAULT NULL,
                                                                             `Secondary_images` text DEFAULT NULL,
                                                                             `videos` text DEFAULT NULL,
                                                                             `Product_benefits` varchar(255) DEFAULT NULL,
                                                                             `Active_ingredients` longtext DEFAULT NULL,
                                                                             `Item_form` varchar(200) DEFAULT NULL,
                                                                             `Flavor` varchar(150) DEFAULT NULL,
                                                                             `Age_range` varchar(200) DEFAULT NULL,
                                                                             `Material_type_free` varchar(200) DEFAULT NULL,
                                                                             `Number_of_items` varchar(100) DEFAULT NULL,
                                                                             `Included_components` varchar(255) DEFAULT NULL,
                                                                             `About_this_item` longtext DEFAULT NULL,
                                                                             `Manufacturer` varchar(200) DEFAULT NULL,
                                                                             `Product_description` text,
                                                                             `Product_details` json DEFAULT NULL,
                                                                             `Important_information` json DEFAULT NULL,
                                                                             `Safety_information` longtext DEFAULT NULL,
                                                                             `Ingredients` text DEFAULT NULL,
                                                                             `Directions` text DEFAULT NULL,
                                                                             `Legal_disclaimer` varchar(200) DEFAULT NULL,
                                                                             `page_save_id` varchar(150) DEFAULT NULL UNIQUE,
                                                                             PRIMARY KEY (`id`));"""
            self.ob2.crsrSql.execute(create_table)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        print('pipelines started')
        try:
            if isinstance(item, AmazonPlItem):
                self.ob1.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, AmazonPdpItem):
                self.ob2.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

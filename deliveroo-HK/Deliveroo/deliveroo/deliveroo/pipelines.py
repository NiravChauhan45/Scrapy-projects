# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import mysql.connector
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import deliveroo.df_config as db
from deliveroo.items import DeliverooItem


class DeliverooPipeline:
    def __init__(self):
        self.cursor = None
        self.conn = None

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=db.host,
            user=db.username,
            password=db.password,
            database=db.database_name
        )
        self.cursor = self.conn.cursor()
        current_date = datetime.now()

        # Format date as year_month_day
        self.formatted_date = current_date.strftime("%Y_%m_%d")
        self.formatted_date = current_date.strftime("%Y_%m_%d")

        # geohash_data_table table
        # try:
        #     geohash_data_table = f"""CREATE TABLE {db.geohash_data} (
        #                           `id` int NOT NULL AUTO_INCREMENT,
        #                           `city` varchar(255) DEFAULT NULL,
        #                           `geo` varchar(255) DEFAULT NULL,
        #                           `status` varchar(25) DEFAULT 'pending',
        #                           PRIMARY KEY (`id`),
        #                           UNIQUE KEY `geo` (`geo`),
        #                           KEY `status` (`status`),
        #                           KEY `geo_2` (`geo`)
        #                         ) ENGINE=InnoDB AUTO_INCREMENT=2302 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
        #     self.cursor.execute(geohash_data_table)
        # except:
        #     pass

        # restaurant_links table
        try:  # restaurant_links_{self.formatted_date}
            link_table = f"""CREATE TABLE `{db.restaurant_links}` (
              `id` int NOT NULL AUTO_INCREMENT,
              `geohash` varchar(255) DEFAULT NULL,
              `vendor_id` varchar(255) DEFAULT NULL,
              `name` blob,
              `url` varchar(255) DEFAULT NULL,
              `status` varchar(25) DEFAULT 'pending',
              `pagesave` varchar(255) DEFAULT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `vendor_id` (`vendor_id`),
              KEY `status` (`status`),
              KEY `url` (`url`),
              KEY `geohash` (`geohash`)
            ) ENGINE=InnoDB AUTO_INCREMENT=4991511 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
            self.cursor.execute(link_table)
        except:
            pass

        # deliveroo_restaurant table
        try:
            restro_data = f"""CREATE TABLE `{db.deliveroo_restaurant}` (
          `scraped_id` int NOT NULL AUTO_INCREMENT,
          `vendor_id` varchar(100) DEFAULT NULL,
          `lead_source` varchar(100) DEFAULT NULL,
          `name` blob,
          `name_local` blob,
          `branch_name` blob,
          `branch_name_local` blob,
          `type` varchar(100) DEFAULT NULL,
          `category` blob,
          `scraped_url` varchar(200) DEFAULT NULL,
          `restaurant_url` varchar(200) DEFAULT NULL,
          `cuisine` varchar(100) DEFAULT NULL,
          `phone_number` varchar(255) DEFAULT NULL,
          `opening_hours` longtext,
          `rating_score` varchar(100) DEFAULT NULL,
          `number_of_ratings` varchar(50) DEFAULT NULL,
          `food_license_number` varchar(100) DEFAULT NULL,
          `country_code` varchar(100) DEFAULT NULL,
          `city` varchar(100) DEFAULT NULL,
          `address` longtext,
          `address_local` longtext,
          `postal_code` varchar(100) DEFAULT NULL,
          `latitude` varchar(100) DEFAULT NULL,
          `longitude` varchar(100) DEFAULT NULL,
          `request_location` varchar(500) DEFAULT NULL,
          `promotions` tinyint(1) DEFAULT NULL,
          `payment_method` varchar(100) DEFAULT NULL,
          `minimum_order_price` varchar(500) DEFAULT NULL,
          `free_delivery_option` tinyint(1) DEFAULT NULL,
          `delivery_fee` varchar(100) DEFAULT NULL,
          `distance` varchar(100) DEFAULT NULL,
          `distance_unit` varchar(100) DEFAULT NULL,
          `delivery_time` varchar(100) DEFAULT NULL,
          `delivery_time_unit` varchar(100) DEFAULT NULL,
          `others` blob,
          `promotion_tags_delivery` longtext,
          `promotion_tags_pickup` longtext,
          `date_of_scrape` varchar(255) DEFAULT NULL,
          `date_of_data_inserted` varchar(255) DEFAULT NULL,
          `is_open` varchar(100) DEFAULT NULL,
          `is_delivery_available` varchar(100) DEFAULT NULL,
          `is_pickup_enabled` varchar(50) DEFAULT NULL,
          `is_halal` varchar(50) DEFAULT NULL,
          `is_meal_for_one` varchar(100) DEFAULT NULL,
          `sales` varchar(100) DEFAULT NULL,
          `request_location_Latitude` varchar(100) DEFAULT NULL,
          `request_location_Longitude` varchar(100) DEFAULT NULL,
          `is_permanently_closed` varchar(100) ,
          `status` varchar(255) DEFAULT 'pending',
          PRIMARY KEY (`scraped_id`),
          UNIQUE KEY `shop_id` (`vendor_id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
            self.cursor.execute(restro_data)
        except:
            pass

        # Menu_details_delivery table
        try:
            menu_details_delivery = f"""CREATE TABLE `{db.data_menu_delivery}` (
                          `id` int NOT NULL AUTO_INCREMENT,
                          `vendor_id` varchar(155) DEFAULT NULL,
                          `lead_source` varchar(255) DEFAULT 'Deliveroo',
                          `menu_id` varchar(355) DEFAULT NULL,
                          `menu_Category` tinyblob,
                          `menu_items` tinyblob,
                          `image_url` varchar(255) DEFAULT NULL,
                          `original_price_Delivery` varchar(255) DEFAULT NULL,
                          `discounted_price_Delivery` varchar(255) DEFAULT NULL,
                          `discount_price_Delivery` varchar(255) DEFAULT NULL,
                          `discount_MOV_Delivery` varchar(255) DEFAULT NULL,
                          `original_price_pickup` varchar(255) DEFAULT NULL,
                          `discounted_price_pickup` varchar(155) DEFAULT NULL,
                          `discount_price_pickup` varchar(255) DEFAULT NULL,
                          `discount_MOV_pickup` varchar(255) DEFAULT NULL,
                          `is_MFO` varchar(255) DEFAULT 'True',
                          `date_of_scrape` varchar(255) DEFAULT NULL,
                          `date_of_data_inserted` varchar(255) DEFAULT NULL,
                          `hashid` varchar(125) DEFAULT NULL,
                          PRIMARY KEY (`id`),
                          UNIQUE KEY `hashid` (`hashid`),
                          KEY `menu_id_key`(`menu_id`)
                        ) ENGINE=InnoDB AUTO_INCREMENT=51939 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
            """
            self.cursor.execute(menu_details_delivery)
        except:
            pass

        # menu_details_pickup table
        try:
            menu_details_pickup = f"""CREATE TABLE `{db.data_menu_pickup}` (
                          `id` int NOT NULL AUTO_INCREMENT,
                          `vendor_id` varchar(155) DEFAULT NULL,
                          `lead_source` varchar(255) DEFAULT 'Deliveroo',
                          `menu_id` varchar(355) DEFAULT NULL,
                          `menu_Category` tinyblob,
                          `menu_items` tinyblob,
                          `image_url` varchar(255) DEFAULT NULL,
                          `original_price_Delivery` varchar(255) DEFAULT NULL,
                          `discounted_price_Delivery` varchar(255) DEFAULT NULL,
                          `discount_price_Delivery` varchar(255) DEFAULT NULL,
                          `discount_MOV_Delivery` varchar(255) DEFAULT NULL,
                          `original_price_pickup` varchar(255) DEFAULT NULL,
                          `discounted_price_pickup` varchar(155) DEFAULT NULL,
                          `discount_price_pickup` varchar(255) DEFAULT NULL,
                          `discount_MOV_pickup` varchar(255) DEFAULT NULL,
                          `is_MFO` varchar(255) DEFAULT 'True',
                          `date_of_scrape` varchar(255) DEFAULT NULL,
                          `date_of_data_inserted` varchar(255) DEFAULT NULL,
                          `hashid` varchar(125) DEFAULT NULL,
                          PRIMARY KEY (`id`),
                          UNIQUE KEY `hashid` (`hashid`)
                        ) ENGINE=InnoDB AUTO_INCREMENT=51939 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
            """
            self.cursor.execute(menu_details_pickup)
        except:
            pass

    def process_item(self, item, spider):
        if isinstance(item, DeliverooItem):
            try:
                field_list = []
                value_list = []
                for field in item:
                    field_list.append(str(field))
                    value_list.append(str(item[field]).replace("'", "’"))
                fields = ','.join(field_list)
                values = "','".join(value_list)
                insert_db = f"insert into {db.deliveroo_restaurant} ( " + fields + " ) values ( '" + values + "' )"
                self.cursor.execute(insert_db)
                self.conn.commit()
                print(insert_db)
                sql = f"update {db.restaurant_links} set `status`='Done1'  where vendor_id={item['vendor_id']};"
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(str(e))
                sql = f"update {db.restaurant_links} set `status`='Dup'  where vendor_id={item['vendor_id']};"
                self.cursor.execute(sql)
                self.conn.commit()

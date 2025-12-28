from datetime import datetime
import nykaa_fashion_weekly.db_config as db
import pymysql
from nykaa_fashion_weekly.config.database_config import ConfigDatabase
from nykaa_fashion_weekly.items import PdpDataItem


class NykaaFashionWeeklyPipeline:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database=db.database_name
    )
    cur = conn.cursor()
    today_date = datetime.now().strftime("%d_%m_%Y")

    def open_spider(self, spider):
        try:
            self.obj = ConfigDatabase(table=f"pdp_data_{db.current_date}", database=db.database_name)
        except Exception as e:
            print(e)

        try:
            create_table = f"""
                CREATE TABLE IF NOT EXISTS `pdp_data_{db.current_date}` (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `product_id` varchar(200) DEFAULT NULL,
                  `catalog_name` text,
                  `catalog_id` text,
                  `source` text,
                  `scraped_date` text,
                  `product_name` text,
                  `image_url` text,
                  `category_hierarchy` text,
                  `product_price` text,
                  `arrival_date` text,
                  `shipping_charges` text,
                  `is_sold_out` varchar(10) DEFAULT NULL,
                  `discount` varchar(10) DEFAULT NULL,
                  `mrp` varchar(10) DEFAULT NULL,
                  `page_url` text,
                  `product_url` text,
                  `number_of_ratings` varchar(10) DEFAULT NULL,
                  `avg_rating` varchar(10) DEFAULT NULL,
                  `position` varchar(10) DEFAULT NULL,
                  `country_code` varchar(10) DEFAULT NULL,
                  `images` longtext,
                  `Best_price` varchar(10) DEFAULT NULL,
                  `Best_offers` text,
                  `bank_offers` varchar(200) DEFAULT NULL,
                  `product_details` text,
                  `specifications` text,
                  `rating` varchar(10) DEFAULT NULL,
                  `MOQ` varchar(10) DEFAULT NULL,
                  `brand` varchar(150) DEFAULT NULL,
                  `product_code` varchar(250) DEFAULT NULL,
                  `Available_sizes` varchar(100) DEFAULT NULL,
                  `sellerPartnerId` varchar(150) DEFAULT NULL,
                  `seller_return_policy` varchar(255) DEFAULT NULL,
                  `manufacturing_info_packerInfo` text,
                  `manufacturing_info_seller_name` text,
                  `manufacturing_info_importerInfo` text,
                  `manufacturing_info_countryOfOrigin` text,
                  `manufacturing_info_manufacturerInfo` text,
                  `More_colours` varchar(100) DEFAULT NULL,
                  `variation_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `product_id` (`product_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
            """
            self.cur.execute(create_table)
            self.conn.commit()
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, PdpDataItem):
                self.obj.insertItemToSql(item)
                mycursor = self.conn.cursor()
                sql = f"UPDATE {db.current_date}_{db.input_name} SET status = %s WHERE product_id = %s"
                values = ('Done', item['product_id'])
                mycursor.execute(sql, values)
                self.conn.commit()
                return item
        except Exception as e:
            print(e)

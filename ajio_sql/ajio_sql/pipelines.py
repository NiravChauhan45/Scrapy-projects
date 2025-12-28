# Define your item pipelines here
from datetime import datetime
import pymysql
from ajio_sql.items import AjioSqlItem
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from ajio_sql.config.database_config import ConfigDatabase
from ajio_sql import config
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import ajio_sql.db_config as db

class AjioSqlPipeline:
    today_date = datetime.strftime(datetime.now(), '%d_%m_%Y')
    conn = pymysql.connect(
        database="ajio",
        user="root",
        host="localhost",
        password="actowiz"
    )
    cur = conn.cursor()

    def open_spider(self, spider):

        try:
            self.ob1 = ConfigDatabase(table=f'product_details_{self.today_date}', database='ajio')
        except Exception as e:
            spider.logger.info(e)

        try:
            create_table = f"""
            CREATE TABLE `product_details_{self.today_date}` (
                  `Id` int NOT NULL AUTO_INCREMENT,
                  `product_id` varchar(200) DEFAULT NULL,
                  `catalog_name` varchar(255) DEFAULT NULL,
                  `catalog_id` varchar(200) DEFAULT NULL,
                  `source` varchar(20) DEFAULT 'Ajio',
                  `scraped_date` datetime DEFAULT CURRENT_TIMESTAMP,
                  `product_name` varchar(255) DEFAULT NULL,
                  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `category_hierarchy` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `product_price` varchar(20) DEFAULT NULL,
                  `arrival_date` varchar(20) DEFAULT NULL,
                  `shipping_charges` varchar(20) DEFAULT NULL,
                  `is_sold_out` varchar(20) DEFAULT NULL,
                  `discount` varchar(20) DEFAULT NULL,
                  `mrp` varchar(20) DEFAULT NULL,
                  `page_url` varchar(255) DEFAULT NULL,
                  `product_url` varchar(265) DEFAULT NULL,
                  `number_of_ratings` varchar(10) DEFAULT NULL,
                  `avg_rating` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `position` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `country_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'IN',
                  `images` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                  `Best_price` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `Best_offers` longtext,
                  `bank_offers` longtext,
                  `product_details` longtext,
                  `specifications` longtext,
                  `rating` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `MOQ` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `brand` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `product_code` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `Available_sizes` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `sellerPartnerId` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `seller_return_policy` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
                  `manufacturing_info_packerInfo` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `manufacturing_info_seller_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `manufacturing_info_importerInfo` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `manufacturing_info_countryOfOrigin` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `manufacturing_info_manufacturerInfo` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `More_colours` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `variation_id` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  PRIMARY KEY (`Id`),
                  UNIQUE KEY `product_id` (`product_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
            """
            self.cur.execute(create_table)
            self.conn.commit()
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, AjioSqlItem):
                self.ob1.insertItemToSql(item)

                try:
                    # update_query = """UPDATE nsm_inputs SET status = %s WHERE product_id = %s"""
                    update_query = f"""UPDATE {db.input_name}_inputs SET status = %s WHERE product_id = %s"""
                    data = ("Done", item['product_id'])  # set age=30 for user with id=1
                    self.cur.execute(update_query, data)
                    self.conn.commit()
                    print(f"Item Successfully Updated...")
                except Exception as error:
                    print(error)

                return item
        except Exception as e:
            print(e)

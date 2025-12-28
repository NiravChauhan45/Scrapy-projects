# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from big_basket_com.items import BigBasketComItem
from big_basket_com.config.database_config import ConfigDatabase
import pymysql
import big_basket_com.db_config as db


class BigBasketComPipeline:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database=db.database_name
    )
    cur = conn.cursor()

    def open_spider(self, spider):
        try:
            self.pdp_data_table = ConfigDatabase(table=f"{db.pdp_data_table}", database=f"{db.database_name}")
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, BigBasketComItem):
                self.pdp_data_table.insertItemToSql(item)
                # Todo: Done-Pending
                try:
                    update_query = f"UPDATE pincodes SET status = %s WHERE pincode = %s"
                    self.cur.execute(update_query, ("Done", item['Pincode']))
                    self.conn.commit()
                except Exception as e:
                    print(e)
                return item
        except Exception as e:
            print(e)

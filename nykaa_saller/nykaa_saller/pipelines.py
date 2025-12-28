# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from nykaa_saller.items import NykaaSallerPlItem, NykaaSallerPdpItem
import nykaa_saller.db_config as db
from nykaa_saller.config.database_config import ConfigDatabase


class NykaaSallerPipeline:
    def open_spider(self, spider):
        try:
            self.url_obj = ConfigDatabase(table=db.link_table, database=db.database_name)
            self.data_obj = ConfigDatabase(table=db.pdp_table, database=db.database_name)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, NykaaSallerPlItem):
                self.url_obj.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, NykaaSallerPdpItem):
                self.data_obj.insertItemToSql(item)
                mycursor = db.conn.cursor()
                sql = f"UPDATE {db.link_table} SET status = %s WHERE product_url = %s"
                values = ('Done', item['Product_Sku_Url'])
                mycursor.execute(sql, values)
                db.conn.commit()
                return item
        except Exception as e:
            print(e)

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import mysql.connector
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from amazon.items import AmazonElviePdpLinkItem
from amazon.config.database_config import ConfigDatabase


class AmazonPipeline:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="amazon"
    )

    def open_spider(self, spider):
        today_date = datetime.now().strftime("%d_%m_%Y")
        try:
            self.ob = ConfigDatabase(table="pdp_links_elvie", database="amazon")
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, AmazonElviePdpLinkItem):
                self.ob.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

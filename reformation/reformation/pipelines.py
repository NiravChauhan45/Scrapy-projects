from itemadapter import ItemAdapter
from reformation.items import ReformationSiteMapPlItem,ReformationVariationItem
import reformation.db_config as db
from reformation.config.database_config import ConfigDatabase


class ReformationPipeline:
    def open_spider(self, spider):
        try:
            self.url_sitemap_obj = ConfigDatabase(table=db.pdp_links_sitemap, database=db.database_name)
            self.variation_obj = ConfigDatabase(table=db.variations_links, database=db.database_name)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        try:
            if isinstance(item, ReformationSiteMapPlItem):
                self.url_sitemap_obj.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

        try:
            if isinstance(item, ReformationVariationItem):
                self.variation_obj.insertItemToSql(item)
                return item
        except Exception as e:
            print(e)

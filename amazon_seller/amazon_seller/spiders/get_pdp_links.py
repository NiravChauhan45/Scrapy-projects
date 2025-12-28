import scrapy
from scrapy import cmdline
from loguru import logger
from amazon_seller.items import AmazonSellerItem
from amazon_seller.config.database_config import ConfigDatabase
import amazon_seller.config.db_config as db_config


class GetPdpLinksSpider(scrapy.Spider):
    name = "get_pdp_links"
    allowed_domains = ["www.amazon.com"]

    def __init__(self, start_index, end, **kwargs):
        super().__init__()
        self.start_index = start_index
        self.end = end
        self.cookies = {
            'session-id': '258-0137535-6740005',
            'i18n-prefs': 'INR',
            'lc-acbin': 'en_IN',
            'ubid-acbin': '262-2354933-0835115',
            'session-token': '+F1hne5L0vHxJXnejm6A9Z+O6U5OCnz6ErcBMpGEwfJZ3/fN7+uV9LqEHMIaLRxQjmsGcVEKNZoOR9YkhMf4mFmqTArGtxncjRGxCmcVJtC6NfGzIZsiFSuRgMv/Bx56PIkTPKf3NVZVS4q8TveLCSsEZ4aIP1sXKyidrQOmWt/TYBeO0l9hJrUXKWyLOairMvISlYP0wH7Z1XWVQo6YzQHOC4tvhYAWRWF78E6Lfj6gzqeHbPbX+6ej/4U9eAB8thynj3n1o46EcHe0uz3qLIm1iVPVhzy44goNBE0MQKT+BcJx+1B3cOZ2YmQ4Gm6QQLsbrYGMpBDI3AaSiDtmdzVwyWXqx+tn',
            'csm-hit': 'tb:FCYVEKNGAVZ7PQW42WEF+s-FCYVEKNGAVZ7PQW42WEF|1752844845789&t:1752844845789&adb:adblk_no',
            'session-id-time': '2082758401l',
            'rxc': 'AOSTHefndzIMTuUqA+k',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'device-memory': '8',
            'downlink': '3.9',
            'dpr': '1',
            'ect': '4g',
            'priority': 'u=0, i',
            'rtt': '150',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'viewport-width': '1920',
        }
        self.item_table = ConfigDatabase(table=db_config.item_table_name,
                                         database=db_config.database_name)

    def start_requests(self):
        results = self.item_table.fetchResultsfromSql(conditions={'status': 'Pending'}, start=self.start_index, end=self.end)
        for result in results:
            item_type = result['item_type']
            item_link = result['item_link']

            yield scrapy.Request(url=item_link, headers=self.headers, cookies=self.cookies,
                                 meta={"item_type": item_type},
                                 dont_filter=True)

    def parse(self, response, **kwargs):
        item_type = response.meta.get("item_type")

        product_urls_list = response.xpath("//a[@class='a-link-normal s-no-outline']/@href").getall()
        for product_url in product_urls_list:
            if product_url:
                item = AmazonSellerItem()
                product_id = product_url.split('/dp/')[-1].split('/ref=')[0]
                product_url = f"https://www.amazon.in/dp/{product_id}"
                # Todo: yield item
                item['item_type'] = item_type
                item['product_id'] = product_id
                item['product_url'] = product_url
                print(item)
                yield item

        # Todo: Next Page Link
        next_page = response.xpath("//a[contains(text(),'Next')]/@href").getall()
        if next_page:
            next_page_link = "".join(["https://www.amazon.in" + link.strip() for link in next_page if link.strip()])
            yield scrapy.Request(url=next_page_link, headers=self.headers, cookies=self.cookies,
                                 meta={"item_type": item_type}, callback=self.parse,
                                 dont_filter=True)
        else:
            cur = db_config.conn.cursor()
            update_query = f"UPDATE {db_config.item_table_name} SET status='Done' WHERE item_type={item_type}"
            cur.execute(update_query)
            db_config.conn.commit()
            logger.success(f"Your this {item_type} item_type successfully updated !")


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {GetPdpLinksSpider.name} -a start_index=2 -a end=2".split())

import hashlib
from typing import Iterable

import scrapy
from scrapy import cmdline, Request
import re
from nuttygritties.config.database_config import ConfigDatabase
from nuttygritties.items import NuttygrittiesUrlItem


class ExtractUrlSpider(scrapy.Spider):
    name = "extract_url"
    allowed_domains = ["www.nuttygritties.com"]

    # start_urls = ["https://www.nuttygritties.com"]
    def __init__(self, **kwargs):  # start=0, end=1000000
        super().__init__(**kwargs)
        self.db = ConfigDatabase(database='nuttygritties', table=f'product_url')

    def start_requests(self):
        yield scrapy.Request(url="https://nuttygritties.com/sitemap_products_1.xml?from=1901146701870&to=7100215820334",
                             callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        item = NuttygrittiesUrlItem()
        text = response.text
        pattern = r"<loc>(https?://[^\s<>]+)</loc>"
        urls = re.findall(pattern, text)
        for url in urls[1:]:
            hash_key = int(hashlib.md5(
                bytes(
                    str(url),
                    "utf8")).hexdigest(),
                           16) % (10 ** 18)
            item['urls'] = url
            item['hash_key'] = hash_key

            yield item


if __name__ == '__main__':
    cmdline.execute("scrapy crawl extract_url".split())

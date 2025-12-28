import re
import pymysql
import scrapy
from scrapy.cmdline import execute
import big_basket.config as db
from big_basket.items import BigbasketLinksItem

# from big_basket.items import BigbasketLinksItem


class PdpLinksSpider(scrapy.Spider):
    name = "pdp_links"
    start_urls = ["https://www.bigbasket.com/sitemap.xml"]
    con = pymysql.connect(host="localhost", user="root", password="actowiz", database="big_basket")
    cursor = con.cursor()

    def parse(self, response):
        links = re.findall('\<loc\>(.*.)\<\/loc\>', response.text)
        for link in links:
            if 'productsitemap' in link:
                yield scrapy.Request(method='GET', url=link, callback=self.parse1)

    def parse1(self, response):
        links = re.findall('\<loc\>(.*.)\<\/loc\>', response.text)
        for link in links:
            item = BigbasketLinksItem()
            item['sitemap_url'] = response.url
            item['product_url'] = link
            yield item


if __name__ == '__main__':
    execute(f"scrapy crawl {PdpLinksSpider.name}".split())

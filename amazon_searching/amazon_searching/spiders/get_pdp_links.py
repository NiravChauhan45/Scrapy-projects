import gzip
import hashlib
import json
import os
import random

import mysql.connector
import scrapy
from scrapy import cmdline

from amazon_searching.config.database_config import ConfigDatabase
from amazon_searching.items import AmazonSearchingPdpItem


class GetPdpLinksSpider(scrapy.Spider):
    name = "get_pdp_links"

    def pagesave_data(self, pagesave_id, response):
        # Todo: page save
        pagesave = r"F:\Nirav\Project_page_save\amazon_search"
        try:
            os.makedirs(pagesave, exist_ok=True)
            main_path = fr'{pagesave}\{pagesave_id}.html.gz'
            if not os.path.exists(main_path):
                with gzip.open(main_path, "wb") as f:
                    f.write(response.text.encode('utf-8'))
                print(f"page save for this {pagesave_id}")
        except Exception as e:
            print(e)

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.db = ConfigDatabase(database='amazon_searching', table='new_category_table')
        self.start = start
        self.end = end
        self.custom_settings = {
            "USER_AGENT": None,
            "DOWNLOAD_HANDLERS": {
                "http": "scrapy_impersonate.ImpersonateDownloadHandler",
                "https": "scrapy_impersonate.ImpersonateDownloadHandler",
            },
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor", }
        self.browser = random.choice(["chrome110", "edge99", "safari15_5"])
        self.cookies = {
            'x-amz-captcha-1': '1740064659874893',
            'x-amz-captcha-2': 'odk+bw8e4WQAhUKpt2xPWA==',
            'session-id': '131-7967661-8597542',
            'session-id-time': '2082787201l',
            'i18n-prefs': 'USD',
            'ubid-main': '131-4199319-4736135',
            'regStatus': 'pre-register',
            'AMCV_7742037254C95E840A4C98A6%40AdobeOrg': '1585540135%7CMCIDTS%7C20159%7CMCMID%7C14261673283856433932800593299618800155%7CMCAAMLH-1742278675%7C12%7CMCAAMB-1742278675%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1741681076s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0',
            'lc-main': 'en_US',
            'session-token': '75FmVJfMpImj3IVon6PYppfA3pmyL6O1gCFumRvgFI60wbOmVfINcO51f8HonurLp73/E1Dsi8WCQomAgJnVC2SvXI7FjSG4F9RPIGChQk1+puo3LQnpe+rltk5RkGViYHt9Ql1MmcCmOtZDVdGpeaghMNEGBlQfIFGkOi7SwPYpNd6/u4oQzNGmKIEM7snxDbD5gKf03G6LT3jDIeqZkZ7FB1aAGJ/xDYhdltmMtEHWmHgqMPwQDbFZiSaahgg5GkvOoKz7l2f7NqK386oKFijMqVlS7AyP6H/xBejL1af+XuxhjHnzTj/0geaCyQIj4Lr6STc3lfdi+bd7YDp9i9AbW2uz1uNv',
            'csm-hit': 'tb:9N5SA7W7RZ2RH7NVAES8+s-3YPNBGBFT80CAQ0D41GE|1742562408824&t:1742562408824&adb:adblk_no',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'device-memory': '8',
            'downlink': '0.15',
            'dpr': '1.35',
            'ect': 'slow-2g',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'rtt': '2200',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'viewport-width': '1422',
            # 'cookie': 'x-amz-captcha-1=1740064659874893; x-amz-captcha-2=odk+bw8e4WQAhUKpt2xPWA==; session-id=131-7967661-8597542; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=131-4199319-4736135; regStatus=pre-register; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C20159%7CMCMID%7C14261673283856433932800593299618800155%7CMCAAMLH-1742278675%7C12%7CMCAAMB-1742278675%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1741681076s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; lc-main=en_US; session-token=75FmVJfMpImj3IVon6PYppfA3pmyL6O1gCFumRvgFI60wbOmVfINcO51f8HonurLp73/E1Dsi8WCQomAgJnVC2SvXI7FjSG4F9RPIGChQk1+puo3LQnpe+rltk5RkGViYHt9Ql1MmcCmOtZDVdGpeaghMNEGBlQfIFGkOi7SwPYpNd6/u4oQzNGmKIEM7snxDbD5gKf03G6LT3jDIeqZkZ7FB1aAGJ/xDYhdltmMtEHWmHgqMPwQDbFZiSaahgg5GkvOoKz7l2f7NqK386oKFijMqVlS7AyP6H/xBejL1af+XuxhjHnzTj/0geaCyQIj4Lr6STc3lfdi+bd7YDp9i9AbW2uz1uNv; csm-hit=tb:9N5SA7W7RZ2RH7NVAES8+s-3YPNBGBFT80CAQ0D41GE|1742562408824&t:1742562408824&adb:adblk_no',
        }
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="actowiz",
            database="amazon_searching"
        )

    def start_requests(self):
        results = self.db.fetchResultsfromSql(start=self.start, end=self.end, conditions={'status': 'pending'})
        for result in results:
            main_category_name = result['main_category_name']
            main_category_url = result['main_category_url']
            category_name = result['category_name']
            category_url = result['category_url']
            sub_category_name = result['sub_category_name']
            sub_category_url = result['sub_category_url']
            hash_id = result['hash_id']

            yield scrapy.Request(url=sub_category_url, headers=self.headers, cookies=self.cookies, dont_filter=True,
                                 callback=self.parse,
                                 meta={'main_category_name': main_category_name, 'main_category_url': main_category_url,
                                       'category_name': category_name, 'hash_id': hash_id,
                                       'category_url': category_url, 'sub_category_name': sub_category_name,
                                       'sub_category_url': sub_category_url, "impersonate": self.browser})

    def parse(self, response, **kwargs):
        pagesave_id = str(
            int(hashlib.md5(
                bytes(response.url, "utf8")).hexdigest(),
                16) % (
                    10 ** 10))
        meta_data = response.meta
        main_category_name = response.meta['main_category_name']
        main_category_url = meta_data['main_category_url']
        category_name = meta_data['category_name']
        category_url = meta_data['category_url']
        sub_category_name = meta_data['sub_category_name']
        sub_category_url = meta_data['sub_category_url']
        hash_id = meta_data['hash_id']
        self.pagesave_data(pagesave_id, response)
        l1 = {'name': main_category_name, 'url': main_category_url}
        l2 = {'name': category_name, 'url': category_url}
        l3 = {'name': sub_category_name, 'url': sub_category_url}
        breadcrumb = [l1, l2, l3]
        for data in response.xpath("//div[@role='listitem']"):
            item = AmazonSearchingPdpItem()
            product_url = "https://www.amazon.com" + data.xpath('.//a[@class="a-link-normal s-no-outline"]/@href').get()
            if '/sspa/' in product_url:
                product_id = product_url.split('dp%2F')[-1].split('%2')[0]
            else:
                product_id = product_url.split('/dp/')[-1].split('/')[0]
            prime_tag = data.xpath(".//span[@class='aok-relative s-icon-text-medium s-prime']/i/@aria-label").get()
            if prime_tag:
                prime_tag = data.xpath(".//span[@class='aok-relative s-icon-text-medium s-prime']/i/@aria-label").get()
            else:
                prime_tag = "NA"
            item['prime_tag'] = prime_tag
            item['product_id'] = product_id
            item['product_url'] = product_url
            item['breadcrumb'] = json.dumps(breadcrumb)
            item['pagesave_id'] = pagesave_id
            yield item

        # Todo: Next page
        if response.xpath("//a[contains(text(),'Next')]/@href"):
            next_page_url = "https://www.amazon.com" + response.xpath("//a[contains(text(),'Next')]/@href").get()
            yield scrapy.Request(url=next_page_url, headers=self.headers, cookies=self.cookies, dont_filter=True,
                                 callback=self.parse,
                                 meta={'main_category_name': main_category_name, 'main_category_url': main_category_url,
                                       'category_name': category_name, 'hash_id': hash_id,
                                       'category_url': category_url, 'sub_category_name': sub_category_name,
                                       'sub_category_url': sub_category_url, "impersonate": self.browser})
        else:
            update_query = f"UPDATE {self.db.table} SET status = %s WHERE hash_id = %s"
            values = ('Done', hash_id)
            cursor = self.conn.cursor()
            cursor.execute(update_query, values)
            self.conn.commit()


if __name__ == '__main__':
    cmdline.execute(f'scrapy crawl {GetPdpLinksSpider.name} -a start=1 -a end=1'.split())

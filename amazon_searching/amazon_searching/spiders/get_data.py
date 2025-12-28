import random
from typing import Iterable

import scrapy
from scrapy import Request, cmdline
from amazon_searching.config.database_config import ConfigDatabase


class GetDataSpider(scrapy.Spider):
    name = "get_data"
    db = ConfigDatabase(database='amazon_prime', table='category_table')

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.db = ConfigDatabase(database='amazon_searching', table='category_links')
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

    def start_requests(self):
        results = self.db.fetchResultsfromSql(start=self.start, end=self.end, conditions={'status': 'pending'})
        for result in results:
            main_category_name = result['main_category_name']
            main_category_url = result['main_category_url']
            category_name = result['category_name']
            category_url = result['category_url']
            cookies = {
                'x-amz-captcha-1': '1740064659874893',
                'x-amz-captcha-2': 'odk+bw8e4WQAhUKpt2xPWA==',
                'session-id': '131-7967661-8597542',
                'session-id-time': '2082787201l',
                'i18n-prefs': 'USD',
                'ubid-main': '131-4199319-4736135',
                'regStatus': 'pre-register',
                'AMCV_7742037254C95E840A4C98A6%40AdobeOrg': '1585540135%7CMCIDTS%7C20159%7CMCMID%7C14261673283856433932800593299618800155%7CMCAAMLH-1742278675%7C12%7CMCAAMB-1742278675%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1741681076s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0',
                'lc-main': 'en_US',
                'session-token': 'lp3zammttFFfG10GEwyvf3LU61WPGrjM47MxwdL/GsethyUQPzAWUSfNmAQG+73zxDiaqAVDC8axB2CHC58HvzEWH819P7U0tnYP57rAimbYRQ873PJ9ZGXFsQsk/5HvkN/hjoC3Xws38SwLyEve6He8wjrUWr3oWMDIUjjUuunTC0p3q64Tr84S51E8gK0jkbYD4wUk88nmwFdsjjJiaVtLcB9q965iNZ5xBKW//GHtL2bEukTpAm2jp9u4sHQk4LOccz32R0+Mp/6F5slGVfb6aYdudrsy8QgWXKWUg9Ps8usCyb1E1if/obxpb34p2+jeTeUGBQVQoORkeRop1gcWgB3YJQz+',
                'csm-hit': 'tb:QHKHRDYM012NBCEE9Y0C+s-QHKHRDYM012NBCEE9Y0C|1742550242633&t:1742550242633&adb:adblk_no',
            }
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'device-memory': '8',
                'downlink': '10',
                'dpr': '1.35',
                'ect': '4g',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'referer': 'https://www.amazon.com/s?k=health+care&i=hpc&rh=n%3A3760901%2Cn%3A3760941&dc&ds=v1%3Ax3FipfCHwLnOyBjcyokejidByCGhdpYD5aRO%2F6FYNtA&crid=1WX24CI9NYA0I&qid=1742545467&rnid=3760901&sprefix=health+care%2Chpc%2C288&ref=sr_nr_n_2',
                'rtt': '50',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'viewport-width': '1422',
                # 'cookie': 'x-amz-captcha-1=1740064659874893; x-amz-captcha-2=odk+bw8e4WQAhUKpt2xPWA==; session-id=131-7967661-8597542; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=131-4199319-4736135; regStatus=pre-register; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C20159%7CMCMID%7C14261673283856433932800593299618800155%7CMCAAMLH-1742278675%7C12%7CMCAAMB-1742278675%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1741681076s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; lc-main=en_US; session-token=lp3zammttFFfG10GEwyvf3LU61WPGrjM47MxwdL/GsethyUQPzAWUSfNmAQG+73zxDiaqAVDC8axB2CHC58HvzEWH819P7U0tnYP57rAimbYRQ873PJ9ZGXFsQsk/5HvkN/hjoC3Xws38SwLyEve6He8wjrUWr3oWMDIUjjUuunTC0p3q64Tr84S51E8gK0jkbYD4wUk88nmwFdsjjJiaVtLcB9q965iNZ5xBKW//GHtL2bEukTpAm2jp9u4sHQk4LOccz32R0+Mp/6F5slGVfb6aYdudrsy8QgWXKWUg9Ps8usCyb1E1if/obxpb34p2+jeTeUGBQVQoORkeRop1gcWgB3YJQz+; csm-hit=tb:QHKHRDYM012NBCEE9Y0C+s-QHKHRDYM012NBCEE9Y0C|1742550242633&t:1742550242633&adb:adblk_no',
            }
            yield scrapy.Request(url=category_url, headers=headers, cookies=cookies, dont_filter=True,
                                 callback=self.parse,
                                 meta={'main_category_name': main_category_name, 'main_category_url': main_category_url,
                                       'category_name': category_name,
                                       'category_url': category_url, "impersonate": self.browser})

    def parse(self, response, **kwargs):
        category_data = response.xpath('//li[@class="a-spacing-micro apb-browse-refinements-indent-2"]')
        for cat_data in category_data:
            sub_category_link = cat_data.xpath(
                '//li[@class="a-spacing-micro apb-browse-refinements-indent-2"]//a/@herf').get()
            print(sub_category_link)


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {GetDataSpider.name} -a start=1 -a end=10".split())

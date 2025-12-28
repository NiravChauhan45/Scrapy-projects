import hashlib
import json
from typing import Iterable

import scrapy
from scrapy import Request, cmdline
from amazon_searching.items import AmazonBeautyCareItem


class DataSpider(scrapy.Spider):
    name = "data"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
            'session-token': 'SBGwBmsElB+BxZgmedzgd7qX3E9tiRmWNqailjnIoaub9y1wop+VP/FqszNXp5AM/DzsWaKLR8uqOLko54N9vkR94CqrUL831XVOc+oGXC9eZNO/c7dvXFnb8DSY/m6OsBjgluwPSy0tbRMoxKPxKIQIGNrierQGLTrQ3S2RN8AeMN6hsCLpFZ2V6cF4yRUZ1Z73cTN4qmkWWUwpOEumselDGvVZQu3zLWaxzpO1FbuGWPKkHiu1tTzQImcyNezJk+M3unXgicXmvtB6lu+4rGulaFO9Ezvn26Mreh5jeV//Foe+zmz7dpJA97Z4qZpUK5BvNPoOlpcbQFtINkTI7zSFYLmG/4gB',
            'csm-hit': 'tb:NPR6X1XTW5RKRR9WSKGY+s-KKRA31E2Y295KT95WQS0|1742800278835&t:1742800278835&adb:adblk_no',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'device-memory': '8',
            'downlink': '7.5',
            'dpr': '1.35',
            'ect': '4g',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://www.amazon.com/s?i=beauty&rh=n%3A3760911&dc&qid=1742798227&ref=sr_ex_n_1&ds=v1%3A3t9z7fmia9pqkyiGMMiASFMa3RZrnO61l%2Ft2gYlQrSQ',
            'rtt': '50',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'viewport-width': '1422',
            # 'cookie': 'x-amz-captcha-1=1740064659874893; x-amz-captcha-2=odk+bw8e4WQAhUKpt2xPWA==; session-id=131-7967661-8597542; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=131-4199319-4736135; regStatus=pre-register; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C20159%7CMCMID%7C14261673283856433932800593299618800155%7CMCAAMLH-1742278675%7C12%7CMCAAMB-1742278675%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1741681076s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; lc-main=en_US; session-token=SBGwBmsElB+BxZgmedzgd7qX3E9tiRmWNqailjnIoaub9y1wop+VP/FqszNXp5AM/DzsWaKLR8uqOLko54N9vkR94CqrUL831XVOc+oGXC9eZNO/c7dvXFnb8DSY/m6OsBjgluwPSy0tbRMoxKPxKIQIGNrierQGLTrQ3S2RN8AeMN6hsCLpFZ2V6cF4yRUZ1Z73cTN4qmkWWUwpOEumselDGvVZQu3zLWaxzpO1FbuGWPKkHiu1tTzQImcyNezJk+M3unXgicXmvtB6lu+4rGulaFO9Ezvn26Mreh5jeV//Foe+zmz7dpJA97Z4qZpUK5BvNPoOlpcbQFtINkTI7zSFYLmG/4gB; csm-hit=tb:NPR6X1XTW5RKRR9WSKGY+s-KKRA31E2Y295KT95WQS0|1742800278835&t:1742800278835&adb:adblk_no',
        }

    def start_requests(self):
        main_category_link = 'https://www.amazon.com/b?node=3760911'
        main_category_name = 'Beauty & Personal Care'
        yield scrapy.Request(url=main_category_link, headers=self.headers, cookies=self.cookies,
                             callback=self.category_data,
                             dont_filter=True,
                             meta={'main_category_name': main_category_name, 'main_category_link': main_category_link})

    def category_data(self, response, **kwargs):
        main_category_name = response.meta.get('main_category_name')
        main_category_url = response.url
        for category_data in response.xpath("//li[@class='a-spacing-micro apb-browse-refinements-indent-2']//a"):
            category_name = category_data.xpath("./span/text()").get('').strip()
            category_url = "https://www.amazon.com" + category_data.xpath("./@href").get('').strip()
            meta = {'main_category_name': main_category_name, 'main_category_url': main_category_url,
                    'category_name': category_name, 'category_url': category_url}
            yield scrapy.Request(url=category_url, headers=self.headers, cookies=self.cookies,
                                 callback=self.sub_category_data,
                                 dont_filter=True,
                                 meta=meta)

    def sub_category_data(self, response, **kwargs):
        main_category_name = response.meta.get('main_category_name')
        main_category_url = response.meta.get('main_category_url')
        category_name = response.meta.get('category_name')
        category_url = response.meta.get('category_url')
        for sub_category_data in response.xpath(
                "//li[@class='a-spacing-micro apb-browse-refinements-indent-2']//a"):
            sub_category_name = sub_category_data.xpath("./span/text()").get('').strip()
            sub_category_url = "https://www.amazon.com" + sub_category_data.xpath("./@href").get('').strip()
            meta = {'main_category_name': main_category_name, 'main_category_url': main_category_url,
                    'category_name': category_name, 'category_url': category_url,
                    'sub_category_name': sub_category_name, 'sub_category_url': sub_category_url}
            yield scrapy.Request(url=sub_category_url, headers=self.headers, cookies=self.cookies,
                                 callback=self.child_category_data,
                                 dont_filter=True,
                                 meta=meta)

    def child_category_data(self, response, **kwargs):
        breadcrumbs = []
        main_category_name = response.meta.get('main_category_name')
        main_category_url = response.meta.get('main_category_url')
        category_name = response.meta.get('category_name')
        category_url = response.meta.get('category_url')
        sub_category_name = response.meta.get('sub_category_name')
        sub_category_url = response.meta.get('sub_category_url')
        breadcrumbs = [{'name': main_category_name, 'url': main_category_url},
                       {'name': category_name, 'url': category_url},
                       {'name': sub_category_name, 'url': sub_category_url}]
        product_count = response.xpath(
            '//h2[@class="a-size-base a-spacing-small a-spacing-top-small a-text-normal"]//span/text()').get('').split(
            'over')[-1].split('results')[0].strip().replace(',', '')
        for child_category_data in response.xpath("//li[@class='a-spacing-micro s-navigation-indent-2']//a"):
            child_category_name = child_category_data.xpath("./span/text()").get('').strip()
            child_category_url = "https://www.amazon.com" + child_category_data.xpath("./@href").get('').strip()
            breadcrumbs.append({'name': child_category_name, 'url': child_category_url})
            item = AmazonBeautyCareItem()
            item['main_category_name'] = main_category_name
            item['main_category_url'] = main_category_url
            item['category_name'] = category_name
            item['category_url'] = category_url
            item['sub_category_name'] = sub_category_name
            item['sub_category_url'] = sub_category_url
            item['child_category_name'] = child_category_name
            item['child_category_url'] = child_category_url
            item['breadcrumbs'] = json.dumps(breadcrumbs)
            item['product_count'] = product_count
            hash_id = str(
                int(hashlib.md5(
                    bytes(str(main_category_name) + str(category_name) + str(sub_category_name) + str(
                        child_category_name), "utf8")).hexdigest(),
                    16) % (
                        10 ** 10))
            item['hash_id'] = hash_id
            breadcrumbs.pop()
            yield item


if __name__ == '__main__':
    cmdline.execute(f'scrapy crawl {DataSpider.name}'.split())

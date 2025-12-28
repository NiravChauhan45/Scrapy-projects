import gzip
import hashlib
import random

import scrapy
import os
from datetime import datetime

from scrapy import cmdline
from amazon_new.config.database_config import ConfigDatabase
from amazon_new.items import AmazonPlItem


class PlPageDataSpider(scrapy.Spider):
    name = "pl_page_data"
    allowed_domains = ["www.amazon.com"]
    # start_urls = ["https://www.amazon.com"]

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
    browser = random.choice(["chrome110", "edge99", "safari15_5"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.today_date = datetime.now().strftime("%d_%m_%Y")
        self.pl_pagesave_path = f'F:\\Nirav\\Project_page_save\\amazon_new\\pl_page_save_path\\'

    def start_requests(self):
        pagination = {'1': '1730260008', '2': '1730259704', '3': '1730260031'}
        for page_count, qid in pagination.items():
            url = f"https://www.amazon.com/s?k=Whitening+kits&page={page_count}&ref=sr_pg_{qid}"
            access_path = f'{self.pl_pagesave_path}page_count_{str(page_count)}.html'
            if os.path.exists(access_path):
                yield scrapy.Request(url=f'file:///{access_path}',
                                     dont_filter=True,
                                     callback=self.parse,
                                     meta={'page_count': page_count, "impersonate": self.browser})

            else:
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'max-age=0',
                    'cookie': '_ga=GA1.1.1660656804.1729616472; _gcl_au=1.1.162818000.1729673784; token=2V0OQX2D4M9CEC5VVPIZESTFI8YBU7CPMF4TEH50NFP1VTDPVD4LEYSS1GSY; csrftoken=hoyV02Gg6Su77FbvDORIGE7Q0N75yBqQ78EJ1ZO6LrCB4R7MCEXNbf0oQ7ZAf1R0; _fbp=fb.1.1729673788701.623873045734384720; website_user_form=true; sessionid=moc5k1z1bl91pwfwkzcii0v49g5d6aac; counter=4; _clck=1y1xw8q%7C2%7Cfqa%7C0%7C1757; _ga_YCWYEKBRMQ=GS1.1.1729743229.6.1.1729743630.57.0.0; _ga_B63L29Q67Z=GS1.1.1729743229.6.1.1729743630.0.0.0; _clsk=1vi3c69%7C1729743631364%7C3%7C1%7Cx.clarity.ms%2Fcollect; i18n-prefs=USD; session-id=145-7800357-9600925; session-id-time=2082787201l; sp-cdn="L5Z9:IN"; ubid-main=131-2316807-8739625',
                    'priority': 'u=0, i',
                    'referer': 'https://kohinoorelectronics.com/shop/home-appliances/',
                    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
                }
                yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True,
                                     meta={'page_count': page_count})


    def parse(self, response, **kwargs):
        page_count = response.meta.get('page_count')
        product_data_lst = response.xpath("//div[contains(@class,'puis-card-container')]")
        item = AmazonPlItem()
        for index, product_data in enumerate(product_data_lst, start=1):
            srp_no = page_count
            page_rank = index
            sponsored = product_data.xpath(".//span[@class='puis-label-popover-default']//text()").get()
            if sponsored:
                sponsored = "Yes"
            else:
                sponsored = "No"

            badge = product_data.xpath(".//span[@class='a-badge-text']//text()").get() if product_data.xpath(
                ".//span[@class='a-badge-text']/text()").get() else "N/A"

            product_url = "https://www.amazon.com" + product_data.xpath(
                ".//a[contains(@class,'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')]/@href").get()

            product_name = product_data.xpath(
                ".//a[contains(@class,'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')]/span/text()").get().strip()

            try:
                price = product_data.xpath(
                    ".//span[@class='a-price']/span[contains(@class,'a-offscreen')]/text()").get().strip().replace('$',
                                                                                                                   '')
            except:
                price = 'N/A'

            try:
                price_per_unit = product_data.xpath(
                    ".//span[@class='a-size-base a-color-secondary']//span[@class='a-offscreen']/text()").get().strip().replace(
                    '$', '')
            except:
                price_per_unit = 'N/A'

            hash_key = int(hashlib.md5(
                bytes(
                    str(product_url),
                    "utf8")).hexdigest(),
                           16) % (10 ** 18)

            item['product_name'] = product_name
            item['product_url'] = product_url
            item['sponsored'] = sponsored
            item['badge'] = badge
            item['page_rank'] = page_rank
            item['srp_no'] = srp_no
            item['Price'] = price
            item['Price_per_unit'] = price_per_unit
            item['hash_key'] = hash_key
            yield item

        # page save
        # try:
        #     if not os.path.exists(self.pl_pagesave_path):
        #         os.makedirs(self.pl_pagesave_path)
        #     main_path = f'{self.pl_pagesave_path}page_count_{str(page_count)}.html.gz'
        #     if not os.path.exists(main_path):
        #         with gzip.open(main_path, 'wb') as f:
        #             f.write(response.text.encode('utf-8'))
        #         print(f"page save for this page_count_{page_count}")
        # except Exception as e:
        #     print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl pl_page_data".split())

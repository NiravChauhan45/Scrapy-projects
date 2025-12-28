import hashlib
import random
from typing import Any, Iterable

import scrapy
from scrapy import Request, cmdline
from scrapy.http import Response
from kohinoor_electronics.items import extract_product_url_item


class GetUrlsSpider(scrapy.Spider):
    name = "extract_product_urls"
    allowed_domains = ["www.kohinoorelectronics.com"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
    browser = random.choice(["chrome110", "edge99", "safari15_5"])

    # start_urls = ["https://www.kohinoorelectronics.com"]

    def start_requests(self):
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        yield scrapy.Request(url='https://kohinoorelectronics.com/shop/', headers=headers, dont_filter=True)

    def parse(self, response, **kwargs):
        category_data_lst = response.xpath("//ul[@id='sidebarNav']/li")
        for category_data in category_data_lst:
            try:
                main_category_name = category_data.xpath("./a/text()").get().strip()
                if "Browse Categories" not in main_category_name and "Accessories" not in main_category_name and "Laptops & Printer" not in main_category_name:
                    main_category_name = main_category_name
                    url_slug = "-".join(main_category_name.lower().split())
                    if "Smart Phone" in main_category_name:
                        url_slug = "mobiles"
                    main_category_url = f"https://kohinoorelectronics.com/shop/{url_slug}"
                    cookies = {
                        '_ga': 'GA1.1.1660656804.1729616472',
                        '_gcl_au': '1.1.162818000.1729673784',
                        '_clck': '1y1xw8q%7C2%7Cfq9%7C0%7C1757',
                        'token': '2V0OQX2D4M9CEC5VVPIZESTFI8YBU7CPMF4TEH50NFP1VTDPVD4LEYSS1GSY',
                        'csrftoken': 'hoyV02Gg6Su77FbvDORIGE7Q0N75yBqQ78EJ1ZO6LrCB4R7MCEXNbf0oQ7ZAf1R0',
                        '_fbp': 'fb.1.1729673788701.623873045734384720',
                        'counter': '3',
                        'website_user_form': 'true',
                        '_ga_B63L29Q67Z': 'GS1.1.1729707223.5.0.1729707223.0.0.0',
                        '_ga_YCWYEKBRMQ': 'GS1.1.1729707224.5.0.1729707224.60.0.0',
                        '_clsk': '1krrz77%7C1729707227634%7C1%7C1%7Cq.clarity.ms%2Fcollect',
                    }
                    headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-language': 'en-US,en;q=0.9',
                        'cache-control': 'max-age=0',
                        # 'cookie': '_ga=GA1.1.1660656804.1729616472; _gcl_au=1.1.162818000.1729673784; _clck=1y1xw8q%7C2%7Cfq9%7C0%7C1757; token=2V0OQX2D4M9CEC5VVPIZESTFI8YBU7CPMF4TEH50NFP1VTDPVD4LEYSS1GSY; csrftoken=hoyV02Gg6Su77FbvDORIGE7Q0N75yBqQ78EJ1ZO6LrCB4R7MCEXNbf0oQ7ZAf1R0; _fbp=fb.1.1729673788701.623873045734384720; counter=3; website_user_form=true; _ga_B63L29Q67Z=GS1.1.1729707223.5.0.1729707223.0.0.0; _ga_YCWYEKBRMQ=GS1.1.1729707224.5.0.1729707224.60.0.0; _clsk=1krrz77%7C1729707227634%7C1%7C1%7Cq.clarity.ms%2Fcollect',
                        'priority': 'u=0, i',
                        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'none',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
                    }
                    yield scrapy.Request(url=main_category_url, headers=headers, cookies=cookies,
                                         meta={'main_category_name': main_category_name,
                                               'main_category_url': main_category_url, "impersonate": self.browser},
                                         callback=self.find_page_count, dont_filter=True)
            except Exception as e:
                print(e)

    def find_page_count(self, response):
        main_category_name = response.meta.get('main_category_name')
        main_category_url = response.meta.get('main_category_url')
        page_count = \
            response.xpath("//p[contains(@class,'font-size-14 text-gray-90')]/text()").get().split('of')[-1].split(
                'results')[0].strip()
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': '_ga=GA1.1.1660656804.1729616472; _gcl_au=1.1.162818000.1729673784; token=2V0OQX2D4M9CEC5VVPIZESTFI8YBU7CPMF4TEH50NFP1VTDPVD4LEYSS1GSY; csrftoken=hoyV02Gg6Su77FbvDORIGE7Q0N75yBqQ78EJ1ZO6LrCB4R7MCEXNbf0oQ7ZAf1R0; _fbp=fb.1.1729673788701.623873045734384720; website_user_form=true; sessionid=moc5k1z1bl91pwfwkzcii0v49g5d6aac; counter=4; _clck=1y1xw8q%7C2%7Cfqa%7C0%7C1757; _ga_YCWYEKBRMQ=GS1.1.1729743229.6.1.1729743630.57.0.0; _ga_B63L29Q67Z=GS1.1.1729743229.6.1.1729743630.0.0.0; _clsk=1vi3c69%7C1729743631364%7C3%7C1%7Cx.clarity.ms%2Fcollect; csrftoken=bgXw5kn9uwQeRdIjJFhKbrc2Ai1WTFBDJnLm3MF1XBcGK394hRCCrwGcyhmcZxZl',
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
        yield scrapy.Request(url=f"{main_category_url}/?show_count={page_count}", headers=headers, dont_filter=True,
                             callback=self.get_product_details,
                             meta={'main_category_name': main_category_name, 'main_category_url': main_category_url,
                                   "impersonate": self.browser})

    def get_product_details(self, response):
        main_category_name = response.meta.get('main_category_name')
        product_data_lst = response.xpath("//h5[contains(@class,'product-item__title')]")
        for index, data in enumerate(product_data_lst):
            product_id = data.xpath("./a/@href").get().split('/')[2]
            product_name = data.xpath("./a/text()").get().strip()
            product_url = data.xpath("./a/@href").get().strip()
            product_url = f"https://kohinoorelectronics.com{product_url}"
            item = extract_product_url_item()
            item['main_category_name'] = main_category_name
            item['product_id'] = product_id
            item['product_name'] = product_name
            item['product_url'] = product_url
            yield item


if __name__ == '__main__':
    cmdline.execute("scrapy crawl extract_product_urls".split())

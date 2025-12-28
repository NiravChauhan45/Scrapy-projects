import hashlib
import json
from typing import Iterable

import scrapy
from scrapy import Request, cmdline
import pandas as pd
from dmart.items import DmartItem


class CategorySpider(scrapy.Spider):
    name = "category"
    allowed_domains = ["www.dmart.in"]
    start_urls = ["https://www.dmart.in"]

    def start_requests(self):
        city_data = {
            'Bangalore': '10677',  # store_id - 10677, pincode - 560102
            'Mumbai': '10151',  # store_id - 10151, pincode - 400063
            'Delhi': ''
        }
        for city_name, storeid in city_data.items():
            if storeid:
                headers = {
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-US,en;q=0.9',
                    'd_info': 'w-20240821_173157',
                    'origin': 'https://www.dmart.in',
                    'priority': 'u=1, i',
                    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'storeid': f'{storeid}',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                    'x-request-id': 'ZWM2OGVlNjgtYTUwMi00ZTUyLWJiZWEtM2QzYzlmZTA5ZDM5fHxTLTIwMjQwODIxXzE3MzE1N3x8LTEwMDI=',
                }
                yield scrapy.Request(url=f'https://digital.dmart.in/api/v1/categories/@top?storeId={storeid}',
                                     headers=headers,
                                     meta={'city_name': city_name, 'store_id': storeid}, callback=self.parse,
                                     dont_filter=True)

    def parse(self, response, **kwargs):
        city_name = response.meta.get('city_name')
        store_id = response.meta.get('store_id')
        json_data = json.loads(response.text)
        for main_category in json_data['catArray']:
            main_category_name = main_category['name']
            for sub_category in main_category['subCatArray']:
                sub_category_name = sub_category['name']
                sub_category_slug = ''
                if sub_category.get('subCatArray'):
                    for child_category in sub_category['subCatArray']:
                        item = DmartItem()
                        child_category_name = child_category['name']
                        child_category_slug = child_category['seoToken']
                        child_category_url = 'https://www.dmart.in/category/' + child_category_slug
                        hash_key = int(hashlib.md5(
                            bytes(
                                str(city_name + main_category_name + sub_category_name + child_category_name + child_category_slug),
                                "utf8")).hexdigest(),
                                       16) % (10 ** 18)

                        item['city_name'] = city_name
                        item['store_id'] = store_id
                        item['main_category_name'] = main_category_name
                        item['sub_category_name'] = sub_category_name
                        item['child_category_name'] = child_category_name
                        item['child_category_slug'] = child_category_slug
                        item['child_category_url'] = child_category_url
                        item['hash_key'] = hash_key
                        yield item
                else:
                    sub_category_slug = sub_category['seoToken']
                    hash_key = int(hashlib.md5(
                        bytes(
                            str(city_name + main_category_name + sub_category_name + sub_category_slug),
                            "utf8")).hexdigest(),
                                   16) % (10 ** 18)

                    item['city_name'] = city_name
                    item['store_id'] = store_id
                    item['main_category_name'] = main_category_name
                    item['sub_category_name'] = sub_category_name
                    item['child_category_name'] = "N/A"
                    item['child_category_slug'] = sub_category_slug
                    item['child_category_url'] = "N/A"
                    item['hash_key'] = hash_key
                    yield item


if __name__ == '__main__':
    cmdline.execute("scrapy crawl category".split())

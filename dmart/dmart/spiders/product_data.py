import hashlib
import json
from typing import Iterable

import scrapy
from scrapy import Request, cmdline
from dmart.config.database_config import ConfigDatabase
import os
from dmart.items import dmart_product_data


class ProductDataSpider(scrapy.Spider):
    name = "product_data"
    allowed_domains = ["www.dmart.in"]
    start_urls = ["https://www.dmart.in"]
    page_save_shop = 'D:\\Nirav_page_save\\dmart\\page_save_product_page\\today\\'

    def __init__(self, **kwargs):  # start=0, end=1000000
        super().__init__(**kwargs)
        # self.page_save_shop = None
        # self.start = start
        # self.end = end
        self.db = ConfigDatabase(database='new_dmart', table=f'category')

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'Pending'})  # start=self.start, end=self.end,
        for result in results:
            city_name = result['city_name']
            pincode = str(result['store_id']).replace('10677', '560102').replace('10151', '400063')
            main_category_name = result['main_category_name']
            sub_category_name = result['sub_category_name']
            child_category_name = result['child_category_name']
            child_category_slug = result['child_category_slug']
            hash_key = result['hash_key']
            page_save_shop = 'D:\\Nirav_page_save\\dmart\\page_save_product_page\\today\\'
            access_path = f'{page_save_shop}{str(hash_key)}.json'

            if os.path.exists(access_path):
                yield scrapy.Request(url=f'file:///{access_path}',
                                     dont_filter=True,
                                     callback=self.parse,
                                     meta={'city_name': city_name, 'pincode': pincode,
                                           'main_category_name': main_category_name,
                                           'sub_category_name': sub_category_name,
                                           'child_category_name': child_category_name,
                                           'hash_key': hash_key})
            else:
                cookies = {
                    'd_info': '%22w-20240821_173157%22',
                    'reqId': '%22ZmU4YmJkOWEtMGU5Yi00M2RkLWIyMjMtMjhiMzQ4MjI3N2ZmfHxTLTIwMjQwODIxXzE3MzE1N3x8LTEwMDI%3D%22',
                    '_ga': 'GA1.1.487238112.1727256766',
                    'recentUserPincodeSearch': '%5B%7B%22uniqueId%22%3A%22%22%2C%22pincode%22%3A%22400053%22%2C%22apiMode%22%3A%22%22%2C%22area%22%3A%22Andheri%20(W)%22%2C%22primaryText%22%3A%22400053%22%2C%22secondaryText%22%3A%22Andheri%20(W)%2C%20Mumbai%22%7D%2C%7B%22uniqueId%22%3A%22%22%2C%22pincode%22%3A%22560102%22%2C%22apiMode%22%3A%22%22%2C%22area%22%3A%22HSR%20Layout%22%2C%22primaryText%22%3A%22560102%22%2C%22secondaryText%22%3A%22HSR%20Layout%2C%20Bengaluru%22%7D%5D',
                    'guest': '%7B%22preferredPIN%22%3A%22400053%22%2C%22preferredStore%22%3A%2210151%22%2C%22preferredCity%22%3A%22Mumbai%22%2C%22preferredArea%22%3A%22Andheri%20(W)%22%2C%22isLoggedIn%22%3Afalse%2C%22isPinSet%22%3A%22true%22%7D',
                    '_ga_3TR7GSPBGF': 'GS1.1.1727327279.10.1.1727329657.0.0.0',
                }

                headers = {
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Connection': 'keep-alive',
                    # 'Cookie': 'd_info=%22w-20240821_173157%22; reqId=%22ZmU4YmJkOWEtMGU5Yi00M2RkLWIyMjMtMjhiMzQ4MjI3N2ZmfHxTLTIwMjQwODIxXzE3MzE1N3x8LTEwMDI%3D%22; _ga=GA1.1.487238112.1727256766; recentUserPincodeSearch=%5B%7B%22uniqueId%22%3A%22%22%2C%22pincode%22%3A%22400053%22%2C%22apiMode%22%3A%22%22%2C%22area%22%3A%22Andheri%20(W)%22%2C%22primaryText%22%3A%22400053%22%2C%22secondaryText%22%3A%22Andheri%20(W)%2C%20Mumbai%22%7D%2C%7B%22uniqueId%22%3A%22%22%2C%22pincode%22%3A%22560102%22%2C%22apiMode%22%3A%22%22%2C%22area%22%3A%22HSR%20Layout%22%2C%22primaryText%22%3A%22560102%22%2C%22secondaryText%22%3A%22HSR%20Layout%2C%20Bengaluru%22%7D%5D; guest=%7B%22preferredPIN%22%3A%22400053%22%2C%22preferredStore%22%3A%2210151%22%2C%22preferredCity%22%3A%22Mumbai%22%2C%22preferredArea%22%3A%22Andheri%20(W)%22%2C%22isLoggedIn%22%3Afalse%2C%22isPinSet%22%3A%22true%22%7D; _ga_3TR7GSPBGF=GS1.1.1727327279.10.1.1727329657.0.0.0',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'x-nextjs-data': '1',
                }
                params = {
                    'token': f'{child_category_slug}',
                }
                url = f'https://www.dmart.in/_next/data/QYVM7GmZCvIMr--e5BJCO/category/{child_category_slug}.json'

                yield scrapy.Request(url=url, cookies=cookies, headers=headers, body=json.dumps(params),
                                     callback=self.parse,
                                     meta={'city_name': city_name, 'pincode': pincode,
                                           'main_category_name': main_category_name,
                                           'sub_category_name': sub_category_name,
                                           'child_category_name': child_category_name,
                                           'hash_key': hash_key})

    def parse(self, response, **kwargs):
        item = dmart_product_data()
        city_name = response.meta.get('city_name')
        pincode = response.meta.get('pincode')
        main_category_name = response.meta.get('main_category_name')
        sub_category_name = response.meta.get('sub_category_name')
        child_category_name = response.meta.get('child_category_name')
        # child_category_slug = response.meta.get('child_category_slug')
        hash_key = response.meta.get('hash_key')

        json_data = json.loads(response.text)
        # print(response.text)
        products_data_lst = json_data.get('pageProps').get('plpData').get('products')
        if products_data_lst is not None:
            for product in products_data_lst:
                try:
                    product_url_slug = product.get('seo_token_ntk')
                    product_id = product.get('productId')
                except Exception as e:
                    product_url_slug = ''
                    product_id = ''
                for product_sku in product['sKUs']:
                    sku_unique_id = product_sku['skuUniqueID']
                    # product_name = str(product_sku['name']).strip().replace(' :', ':').replace('  ', '')
                    product_name = str(product_sku['name']).strip()
                    product_url = f'https://www.dmart.in/product/{product_url_slug}?selectedProd={sku_unique_id}'
                    if product_sku['invType'] == 'A':
                        stock = 'in stock'
                    else:
                        stock = 'out stock'
                    new_hash_key = int(hashlib.md5(
                        bytes(
                            str(city_name + product_url + sku_unique_id),
                            "utf8")).hexdigest(),
                                       16) % (10 ** 18)

                    item['city_name'] = city_name
                    item['Pincode'] = pincode
                    item['main_category_name'] = main_category_name
                    item['sub_category_name'] = sub_category_name
                    item['child_category_name'] = child_category_name
                    item['Product_ID'] = product_id
                    item['sku_unique_id'] = sku_unique_id
                    item['Instock'] = stock
                    item['Url'] = str(product_url).strip()
                    item['Name'] = product_name.strip()
                    item['new_hash_key'] = new_hash_key
                    item['page_save_id'] = hash_key
                    yield item

                    # Done/Pending
                    try:
                        self.db.crsrSql.execute(
                            f"update {self.db.table} set status='Done' where hash_key = '{hash_key}'")
                        self.db.connSql.commit()
                        print(f"Status for :{hash_key} Updated=Done")
                    except Exception as e:
                        print(e)
        # page save
        try:
            if not os.path.exists(self.page_save_shop):
                os.makedirs(self.page_save_shop)
            main_path = f'{self.page_save_shop}{str(hash_key)}.json'
            if not os.path.exists(main_path):
                with open(main_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"page save for this {hash_key}")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl product_data".split())  # -a start=0 -a end=1000000

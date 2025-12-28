import hashlib
import json
import os
import re
from datetime import datetime

from scrapy import cmdline
from nuttygritties.items import NuttygrittiesNewProductItem
from nuttygritties.config.database_config import ConfigDatabase
import pandas as pd

import scrapy


class NewProductDataSpider(scrapy.Spider):
    name = "new_product_data"
    allowed_domains = ["www.nuttygritties.com"]
    start_urls = ["https://www.nuttygritties.com"]
    today = datetime.now().strftime("%d_%m_%Y")
    page_save_products = f"F:\\Nirav\\Project_page_save\\nuttygritties\\page_save_product_page\\{today}\\"

    def __init__(self, **kwargs):  # start=0, end=1000000
        super().__init__(**kwargs)
        self.db = ConfigDatabase(database='nuttygritties', table=f'product_url')

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'Pending'})
        for result in results:
            url = result['urls']
            hash_key = result['hash_key']
            page_save_products = "F:\\Nirav\\Project_page_save\\nuttygritties\\page_save_product_page\\"
            access_path = f'{page_save_products}{str(hash_key)}.html'
            if os.path.exists(access_path):
                yield scrapy.Request(url=f'file:///{access_path}',
                                     dont_filter=True,
                                     callback=self.parse,
                                     meta={'url': url, 'hash_key': hash_key})
            else:
                cookies = {
                    'secure_customer_sig': '',
                    'localization': 'IN',
                    '_tracking_consent': '%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22INGJ%22%2C%22reg%22%3A%22%22%7D',
                    '_cmp_a': '%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D',
                    '_shopify_y': '4a5e8623-061c-4232-914c-3b8f89f6d373',
                    '_orig_referrer': 'https%3A%2F%2Fwww.google.com%2F',
                    '_landing_page': '%2Fcollections%2Fraw-almonds',
                    'refb': '1a23388f-75b5-4c3c-a786-f7550e84c971',
                    '_gid': 'GA1.2.399135969.1727336877',
                    '_gcl_au': '1.1.180090999.1727336878',
                    '_fbp': 'fb.1.1727336877811.921836183436355982',
                    '_scid': 'ZoMvkFkqFlHFx-d4FbhIKZGY6xqDpWa2',
                    '_ScCbts': '%5B%5D',
                    '_sctr': '1%7C1727289000000',
                    'receive-cookie-deprecation': '1',
                    'ssid': 'ab4c56fa-015e-4590-ab41-35bac71af74f',
                    '_clck': 'hf7jbs%7C2%7Cfpj%7C0%7C1730',
                    '_ga_2PHZSTNB3L': 'deleted',
                    '_shopify_sa_p': '',
                    'keep_alive': 'e7be81aa-be24-41ad-b393-03d3c3c362a2',
                    '_shopify_s': 'fb2287c6-069e-4b0d-a5a1-decd6bf766fc',
                    '_shopify_sa_t': '2024-09-27T11%3A27%3A07.796Z',
                    '_ga_2HQR80TZ5G': 'GS1.1.1727430303.8.1.1727436427.60.0.0',
                    '_ga_2PHZSTNB3L': 'GS1.1.1727430303.10.1.1727436428.0.0.0',
                    '_ga': 'GA1.2.284946748.1727336877',
                    '_scida': 'm21KXoYjBhw_MphMO4-J9tNzBtjGnWDS',
                    'fsb_previous_pathname': '/collections/salted-almonds/products/jumbo-roasted-almonds-lightly-salted-200g-pack-of-5',
                    '_scsrid_r': '',
                    '_scid_r': 'jQMvkFkqFlHFx-d4FbhIKZGY6xqDpWa20KBVDM_tSl6GIwYcPzKYTDuPifbTcwbYsK5Yv_Z3ltk',
                    '_clsk': '1scwrh4%7C1727437539616%7C23%7C1%7Co.clarity.ms%2Fcollect',
                }
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'max-age=0',
                    # 'cookie': 'secure_customer_sig=; localization=IN; _tracking_consent=%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22INGJ%22%2C%22reg%22%3A%22%22%7D; _cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D; _shopify_y=4a5e8623-061c-4232-914c-3b8f89f6d373; _orig_referrer=https%3A%2F%2Fwww.google.com%2F; _landing_page=%2Fcollections%2Fraw-almonds; refb=1a23388f-75b5-4c3c-a786-f7550e84c971; _gid=GA1.2.399135969.1727336877; _gcl_au=1.1.180090999.1727336878; _fbp=fb.1.1727336877811.921836183436355982; _scid=ZoMvkFkqFlHFx-d4FbhIKZGY6xqDpWa2; _ScCbts=%5B%5D; _sctr=1%7C1727289000000; receive-cookie-deprecation=1; ssid=ab4c56fa-015e-4590-ab41-35bac71af74f; _clck=hf7jbs%7C2%7Cfpj%7C0%7C1730; _ga_2PHZSTNB3L=deleted; _shopify_sa_p=; keep_alive=e7be81aa-be24-41ad-b393-03d3c3c362a2; _shopify_s=fb2287c6-069e-4b0d-a5a1-decd6bf766fc; _shopify_sa_t=2024-09-27T11%3A27%3A07.796Z; _ga_2HQR80TZ5G=GS1.1.1727430303.8.1.1727436427.60.0.0; _ga_2PHZSTNB3L=GS1.1.1727430303.10.1.1727436428.0.0.0; _ga=GA1.2.284946748.1727336877; _scida=m21KXoYjBhw_MphMO4-J9tNzBtjGnWDS; fsb_previous_pathname=/collections/salted-almonds/products/jumbo-roasted-almonds-lightly-salted-200g-pack-of-5; _scsrid_r=; _scid_r=jQMvkFkqFlHFx-d4FbhIKZGY6xqDpWa20KBVDM_tSl6GIwYcPzKYTDuPifbTcwbYsK5Yv_Z3ltk; _clsk=1scwrh4%7C1727437539616%7C23%7C1%7Co.clarity.ms%2Fcollect',
                    'if-none-match': '"cacheable:feab4d26aae710aeb5e0dff04ef00980"',
                    'priority': 'u=0, i',
                    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                }
                yield scrapy.Request(
                    url=url,
                    cookies=cookies, headers=headers,
                    dont_filter=True, callback=self.parse,
                    meta={'url': url, 'hash_key': hash_key})

    def parse(self, response, **kwargs):
        # global variables
        global quantity, unit_price, discount_percentage, discount_amount

        url = response.meta.get('url')
        hash_key = response.meta.get('hash_key')
        json_data = str(response.text).split('var product = {')
        j_data = json.loads("{" + json_data[1].split('};')[0] + "}")

        platform = "Nutty Gritties"  # j_data.get('vendor')
        category_name = j_data.get('type')
        date = datetime.now().strftime("%d-%m-%Y")
        SKU = ""
        Brand = "Nutty Gritties"
        pincode = "NA"

        # product_name
        try:
            product_name = response.xpath("//header[@class='product-title']/h1/span/text()").get()
        except Exception as e:
            product_name = str(j_data.get('title'))

        # product_url
        try:
            product_url = url
        except Exception as e:
            product_url = ''

        # product_id
        try:
            product_id = j_data.get('id')
        except Exception as e:
            product_id = ''

        # selling_price
        try:
            selling_price = j_data.get('price') / 100
        except Exception as e:
            selling_price = response.xpath(
                "//div[@class='prices']/span[@class='price on-sale']/text()").get().strip().replace(
                '₹ ',
                '').replace(',', '')

        # mrp
        try:
            mrp = j_data.get('compare_at_price') / 100
        except Exception as e:
            mrp = response.xpath("//div[@class='prices']/span[@class='compare-price']/text()").get().strip().replace(
                '₹ ',
                '').replace(
                ',', '')

        # quantity, unit price, discount_amount, discount_percentage
        try:
            pattern = r'(\d+\s*(kg|g)|(\d+.\d*(kg)|(\d+.\d*\s(kg))|\d+.\d*(Kg)))\b'
            matches = re.findall(pattern, product_name)

            # quantity
            if matches:
                product_quantity = matches[-1][0]
                qunty = re.search(r'\d+(\.\d+)?', product_quantity).group(0)
                if "kg" in product_quantity or "kgs" in product_quantity or "Kgs" in product_quantity or "Kg" in product_quantity:
                    quantity = float(qunty) * 1000
                else:
                    quantity = float(qunty)
            else:
                print("Quantity not found.")

            # unit price
            if quantity > 0:  # NOTE: selling_price/product_quantity
                unit_price = float(selling_price) / float(quantity)
                unit_price = int(unit_price * 100) / 100
            else:
                unit_price = None

            # discount_amount
            discount_amount = mrp - selling_price
            if discount_amount == 0.0:
                discount_amount = 0

            # discount_percentage
            if mrp != 0:
                discount_percentage = round(((mrp - selling_price) / mrp) * 100)
            else:
                discount_percentage = 'NA'

            discount_percentage = discount_percentage if discount_percentage != 0 else 'NA'
        except Exception as e:
            print(e)

        # stock
        try:
            stock = j_data.get('available')
            if stock:
                stock = 1
            else:
                stock = 0
        except Exception as e:
            try:
                stock = response.xpath(
                    "//div[@class='product-label']/strong[@class='sold-out label']/text()").get().strip()
                stock = 0
            except Exception as e:
                stock = 1

        # item
        item = NuttygrittiesNewProductItem()
        item['platform'] = platform
        item['category_name'] = category_name
        item['date'] = date
        item['SKU'] = SKU
        item['Brand'] = Brand
        item['Pincode'] = pincode
        item['Product_name'] = product_name
        item['Product_id'] = product_id
        item['Product_url'] = product_url
        item['Mrp'] = mrp
        item['Selling_price'] = selling_price
        item['Unit_price'] = unit_price
        item['Discount_percentage'] = discount_percentage
        item['Discount_amount'] = discount_amount
        item['Stock'] = stock
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
            if not os.path.exists(self.page_save_products):
                os.makedirs(self.page_save_products)
            main_path = f'{self.page_save_products}{str(hash_key)}.html'
            if not os.path.exists(main_path):
                with open(main_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"page save for this {hash_key}")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl new_product_data".split())

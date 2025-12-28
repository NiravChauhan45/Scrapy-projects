import gzip
import json
import os
import random
import re
from datetime import datetime
from typing import Any

from scrapy.http import Response

from big_basket.config.database_config import ConfigDatabase
import requests
import scrapy
from scrapy import cmdline, Selector
from big_basket.items import BigbasketPdpDataItem
import mysql.connector


class PdpLinksSpider(scrapy.Spider):
    name = "pdp_data"
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="big_basket"
    )

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.today_date = datetime.now().strftime('%d_%m_%Y')
        self.pagesave = f"F:\\Nirav\\Project_page_save\\big_basket\\pdp\\12-02-2025\\"
        self.db = ConfigDatabase(database="big_basket", table='pdp_links')
        self.custom_settings = {
            "DOWNLOAD_HANDLERS": {
                "http": "scrapy_impersonate.ImpersonateDownloadHandler",
                "https": "scrapy_impersonate.ImpersonateDownloadHandler",
            },
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        }
        self.browser = random.choice(["chrome110", "edge99", "safari15_5"])

    def start_requests(self):
        url = 'https://www.google.com'
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response, **kwargs):
        results = self.db.fetchResultsfromSql(conditions={'status': 'pending'}, start=self.start, end=self.end)
        for result in results:
            product_id = result['product_url'].split('/pd/')[-1].split('/')[0]
            id = result['id']
            url = f'https://www.bigbasket.com/pd/{product_id}/'
            headers = {
                # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                # 'accept-language': 'en-US,en;q=0.9',
                # 'cache-control': 'no-cache',
                # 'cookie': 'ufi=1; bigbasket.com=c5df7103-d932-4007-a064-8c604682b1e0; x-entry-context-id=100; x-entry-context=bb-b2c; _bb_locSrc=default; x-channel=web; _bb_bhid=; _bb_nhid=1723; _bb_vid=NTkwODMwNTk3NTc4OTUyMTc0; _bb_dsevid=; _bb_dsid=; _bb_cid=1; csrftoken=8FVCSybIgtgRyWfaINKkYHsg0FOjqmtH1Jt6DqF2dFQ5u8xmIIV50yN4vTxEbwNo; _bb_home_cache=f580bb19.1.visitor; _bb_bb2.0=1; _is_tobacco_enabled=0; _is_bb1.0_supported=0; bb2_enabled=true; jarvis-id=c69e6146-d4c8-433b-84b9-356a098d7135; _gcl_au=1.1.2136135866.1739283290; _gid=GA1.2.446719943.1739283290; _fbp=fb.1.1739283290100.306883357777220261; csurftoken=hW0BXw.NTkwODMwNTk3NTc4OTUyMTc0.1739283448607.OZl9lgvcSXN7zdw/eYAuhKEAe9qXn4h/JGguYRXTbaE=; adb=0; _bb_lat_long=MTIuOTc2NTk0NHw3Ny41OTkyNzA4; _bb_aid="MzAwNDkxOTI2MA=="; is_global=0; _bb_addressinfo=MTIuOTc2NTk0NHw3Ny41OTkyNzA4fFNoYW50aGFsYSBOYWdhcnw1NjAwMDF8QmVuZ2FsdXJ1fDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==; _bb_pin_code=560001; _bb_sa_ids=14979; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xNDk3OQ==; is_integrated_sa=1; ts=2025-02-11%2019:47:59.664; _ga_FRRYG5VKHX=GS1.1.1739283290.1.1.1739283321.29.0.0; _ga=GA1.2.1872244689.1739283290; _bb_addressinfo=MTIuOTc2NTk0NHw3Ny41OTkyNzA4fFNoYW50aGFsYSBOYWdhcnw1NjAwMDF8QmVuZ2FsdXJ1fDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==; _bb_bb2.0=1; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xNDk3OQ==; _bb_pin_code=560001; _bb_sa_ids=14979; _is_bb1.0_supported=0; _is_tobacco_enabled=0; bb2_enabled=true; csurftoken=hW0BXw.NTkwODMwNTk3NTc4OTUyMTc0.1739283448607.OZl9lgvcSXN7zdw/eYAuhKEAe9qXn4h/JGguYRXTbaE=; is_global=0; is_integrated_sa=1; x-channel=web',
                # 'pragma': 'no-cache',
                # 'priority': 'u=0, i',
                # 'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
                # 'sec-ch-ua-mobile': '?0',
                # 'sec-ch-ua-platform': '"Windows"',
                # 'sec-fetch-dest': 'document',
                # 'sec-fetch-mode': 'navigate',
                # 'sec-fetch-site': 'same-origin',
                # 'sec-fetch-user': '?1',
                # 'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse1, dont_filter=True,
                                 meta={"product_id": product_id, "id": id, "impersonate": self.browser,"dont_redirect":False})

    def parse1(self, response, **kwargs):
        item = BigbasketPdpDataItem()
        id = response.meta.get('id')
        if response.status == 200:
            currently_unavailable = response.xpath("//*[contains(text(),'Currently Unavailable')]/text()").get()
            if currently_unavailable:
                mycursor = self.conn.cursor()
                sql = f"UPDATE pdp_links SET status = 'unavailable' WHERE id = {id}"
                mycursor.execute(sql)
                self.conn.commit()
            else:
                data = json.loads(
                    response.xpath(
                        '''//script[contains(text(), '{"props":{"pageProps":{')]//text()''').get())

                product_id = response.meta.get('product_id')
                filepath = self.pagesave + f"{product_id}.html.gz"
                # Todo: pagesave
                os.makedirs(self.pagesave, exist_ok=True)
                with gzip.open(filepath, 'w') as f:
                    json_data = json.dumps(data).encode('utf-8')
                    f.write(json_data)

                id = response.meta.get('id')
                product_name = "N/A"
                attributes = "N/A"
                if data['props']['pageProps']['productDetails']['children'][0]['desc']:
                    desc = data['props']['pageProps']['productDetails']['children'][0]['desc']
                    if data['props']['pageProps']['productDetails']['children'][0]['brand']['name']:
                        brand = data['props']['pageProps']['productDetails']['children'][0]['brand']['name']
                        desc = brand + " " + desc
                    product_name = desc
                if data['props']['pageProps']['productDetails']['children'][0]['w']:
                    pack_desc = None
                    if data['props']['pageProps']['productDetails']['children'][0]['pack_desc']:
                        pack_desc = data['props']['pageProps']['productDetails']['children'][0]['pack_desc']
                    w = data['props']['pageProps']['productDetails']['children'][0]['w']
                    if pack_desc:
                        w = w + " " + pack_desc
                    attributes = w

                # item = dict()
                item['Product Code'] = data['props']['pageProps']['productDetails']['children'][0]['id']
                # Extracting Product Name :-
                item['Product Name'] = product_name
                item['id'] = id

                # Extracting Attributes :-
                item['Attributes'] = attributes

                # Extracting MRP
                try:
                    mrp = data['props']['pageProps']['productDetails']['children'][0]['pricing']['discount']['mrp']
                    item['MRP'] = float(mrp)
                except:
                    item['MRP'] = "N/A"

                # Extracting Discount
                try:
                    discount = data['props']['pageProps']['productDetails']['children'][0]['pricing']['discount'][
                        'd_text']
                    item['Discount'] = discount
                except:
                    item['Discount'] = "N/A"

                if item['Discount']:
                    pass
                else:
                    item['Discount'] = "N/A"

                if 'add' in data['props']['pageProps']['productDetails']['children'][0]['availability'][
                    'button'].lower():
                    item['Availability'] = True
                else:
                    item['Availability'] = False

                # Extract breadcrumb Category, Sub Category, Other Category
                breadcrumb = data['props']['pageProps']['productDetails']['children'][0]['breadcrumb']
                category_hierarchy = {f"l{index + 1}": category['name'].capitalize() for index, category in
                                      enumerate(breadcrumb)}
                try:
                    item['Category'] = category_hierarchy['l1']
                except:
                    item['Category'] = "N/A"
                try:
                    item['Sub Category'] = category_hierarchy['l2']
                except:
                    item['Sub Category'] = "N/A"
                try:
                    item['Other Category'] = category_hierarchy['l3']
                except:
                    item['Other Category'] = "N/A"

                # Extract breadcrumb Selling Price :-
                try:
                    product_price = \
                        data['props']['pageProps']['productDetails']['children'][0]['pricing']['discount'][
                            'prim_price'][
                            'sp']
                    item['Selling Price'] = float(product_price)
                except:
                    item['Selling Price'] = "N/A"

                # Extract breadcrumb Image URL :-
                try:
                    all_images = [image['xxl'] for image in
                                  data['props']['pageProps']['productDetails']['children'][0]['images']]
                    item['Image URL'] = " | ".join(all_images)
                except:
                    item['Image URL'] = "N/A"

                # Extract About Product, Other Info
                product_specification = "N/A"
                manufacturing_info = "N/A"
                for information in data['props']['pageProps']['productDetails']['children'][0]['tabs']:
                    if 'Other Product Info' == information['title']:
                        content_selector = Selector(text=information['content'])
                        content_selector.xpath('//style').remove()
                        manufacturing_info = [re.sub('\\s+', ' ', product_info).strip() for product_info in
                                              content_selector.xpath('.//text()').getall() if
                                              re.sub('\\s+', ' ', product_info).strip()]
                        if manufacturing_info:
                            manufacturing_info = " ".join(manufacturing_info)
                    elif 'About the Product' == information['title']:
                        text = re.sub('<head>.*<\/head>', '', re.sub('\\s+', ' ', information['content']))
                        content_selector = Selector(text=text)
                        values = " ".join(content_selector.xpath('//div//text()').getall())
                        # print(values)
                        values = re.sub('\\s+', ' ', values).strip()
                        product_specification = values
                    else:
                        text = re.sub('<head>.*<\/head>', '', re.sub('\\s+', ' ', information['content']))
                        content_selector = Selector(text=text)
                        values = " ".join(content_selector.xpath('//div//text()').getall())
                        # print(values)
                        values = re.sub('\\s+', ' ', values).strip()
                        if 'About the Product'.lower() in values.lower():
                            if product_specification == "N/A":
                                product_specification = values.replace('About the Product', '').strip()

                item['About Product'] = product_specification
                item['Other Info'] = manufacturing_info
                description_json = dict()
                description_json['other_info'] = item['Other Info']
                description_json['about_product'] = item['About Product']
                item['Description JSON'] = json.dumps(description_json)

                # Extract breadcrumb Image URL :-
                scrape_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                item['Product URL'] = f"https://www.bigbasket.com/pd/{product_id}/"
                # item['Scrape Time'] = scrape_time
                return item
        else:
            pass


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PdpLinksSpider.name} -a start=0 -a end=210000".split())

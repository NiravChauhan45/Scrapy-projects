import hashlib
import json
import os
import random
import re
from datetime import datetime
from typing import Iterable, Any

import loguru
import mysql.connector
import requests
import scrapy
from parsel import Selector
from scrapy import cmdline, Request
from scrapy.http import Response
from nykaa_fashion.items import NykaaPdpLinksItem
from nykaa_fashion.config.database_config import ConfigDatabase

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="nykaa_fashion"
)


# from nykaa.items import NykaaPdpLinksItem


class NykaaPdpLinksSpider(scrapy.Spider):
    name = "p_links"
    start_urls = ["https://www.nykaa.com"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
    browser = random.choice(["chrome110", "edge99", "safari15_5"])

    handle_httpstatus_list = [400, 404, 500]

    def get_rating(self, selector):
        rating = selector.xpath(
            "//h2[@data-at='customer-reviews']/following-sibling::*//div[@data-at='product-rating']/text()").get(
            '').strip()
        if rating:
            return rating
        else:
            rating = selector.xpath("//div[@class='css-xoezkq']/text()").get('').strip()
            if rating:
                return rating
            else:
                "NA"

    def get_description(self, selector):
        description = selector.xpath("//div[@class='css-1392ehc']//div[@class='css-1obcna']/text()").get('').strip()
        return description

    def get_all_images(self, product_data):
        if product_data.get('plp_pdp_bridge'):
            images_urls_lst = product_data.get('plp_pdp_bridge').get('images')
            if images_urls_lst:
                image_list = []
                for image_url in images_urls_lst:
                    image_list.append(image_url.get('url'))
                return " | ".join(image_list)
        return 'NA'

    def get_offer(self, product_data):
        offer_lst = product_data.get('offers')
        offer_dict = {}
        offer_l = []
        if offer_lst:
            for offer in offer_lst:
                offer_dict['Name'] = offer.get('name')
                offer_dict['Description'] = offer.get('description')
                offer_l.append(offer_dict)
                return json.dumps(offer_l)
        else:
            return json.dumps(dict())

    def get_size_chart(self, product_data):
        if product_data.get('plp_pdp_bridge'):
            if product_data.get('plp_pdp_bridge').get('variants'):
                size_chart_lst = product_data.get('plp_pdp_bridge').get('variants').get('size')
                size_chart = []
                for size in size_chart_lst:
                    size_chart.append(size.get('name'))
                return " | ".join(size_chart)
            else:
                return "NA"
        else:
            return "NA"

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.today_date = datetime.now().strftime('%d_%m_%Y')
        self.db = ConfigDatabase(database="nykaa_fashion", table='new_category_links_with_brand_id')  # cat_links
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'cookie': 'mp_0cd3b66d1a18575ebe299806e286685f_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A1951873daa26c1-0d041970345f76-26011b51-e1000-1951873daa36c1%22%2C%22%24device_id%22%3A%20%221951873daa26c1-0d041970345f76-26011b51-e1000-1951873daa36c1%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; bcookie=90cc4177-75a6-4d0a-a81b-5fd8ae22e36e; EXP_plp-quick-filters=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; tm_stmp=1739872087363; rum_abMwebSort=82; _gcl_au=1.1.1270484231.1739872088; PHPSESSID=68c98693ea33463ab85984a233d2eb5c; _ga=GA1.1.1224715628.1739872088; NYK_VISIT=90cc4177-75a6-4d0a-a81b-5fd8ae22e36e~1739872087862; WZRK_G=ef3c736df620464da0bd47178ba8d5f9; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; _clck=1nwkbdt%7C2%7Cftj%7C0%7C1875; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; bm_sz=5E15D9DD74504D9DB66208FA861272F5~YAAQNnLBFzs3CxOVAQAAgah3GBrXbe36375VUN91LGcgB84mseqQUyctH3adj5kWe8O9hzmqf5KSs1ArVx0TxaDg1uXdNV6I61QsPhmpZTojnMlbMS3NTI0B3VprxnldmJ0EbVxYAk31eoVKJzXtZWz8QN5Airfhqe5++Gp2zgIjZED+ZieDFeiQSRyrjxfTUXYlz8fkUaIICILuC1hF66KVSIFy8IVprFCrZPtZkjAOFRA2rXRutzyUsv4wXvmyruKfscQu89zJlpVvMhu9n0CwWRjOp6C77tuokLecqY+QGZeMcYTYm0URraTIygBENKaWjzr9aaCUl1sUQmx167JRQhRiZzvQuF/LZQboehCf8qBVGlL98o4ehlntQam0m9wqvLpFmg45nnczHzGcnp1NpMnCgIQvJbgHIlO7rB+LBkRwnXPkVoQiPqhHZBQu/t/VyB+WmjTvVuvO9ABo7SPkzwxs8Tyq7sJoYuzhkBTj7mNa4sRdty67blkc9R8M+bhtRcw6YYJaxXKB1RU=~3749688~3487814; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQNnLBF3I3CxOVAQAAGap3GA2BZ1DxQpEna3XYJkXxCHw50LWRChJ8b9YpQigeig/CCXnZ3AbesctkeelZ3k91Vgm6RTsD00WtmOaSb/BHM3AJ2ZaSOi5zXgBWmx2m74nv67Uc2hQDRJsBN3Zpb1iwM1eQvdoeljgWGtN8+aM2/5vk7z/Tc2pm+JpdUT4HdRpl0DrZtK+3GwLEEt/83V+Z8a4Den1olqyLbr0/WbCnBjY1AIbNvazhij7+Z/YY8CfbH/i4cnjPdI76Xxqp0L1l2g0R6Oz157c2MfXr5N1NGNvcN24bd/YBkjxxtrCGq4CB/sNvY9oBZnn/CZwZS+6StTgEkj7jBI6uOdR3463b5rQPHHtca0/OBaYNIyIl7R8rnRjaXvvgyL3htipA9V8Wj2Yu0L1R+4szfuua7UCZQlZ1h8kzr2unGyFVknProKy456yHkbKKcYlYtFqKOT57Qq7McosbPsvCJNhRsIIUK0CJUD3GmKfO7WnO0c6FwUuj6/6oDSwsDM1mAMtJUSg2t/8EB09ZTGpVReULXQ==~-1~-1~1739874099; NYK_PCOUNTER=3; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A12%2C%22s%22%3A1739870502%2C%22t%22%3A1739872124%7D; _clsk=hmipmq%7C1739872126692%7C5%7C0%7Ck.clarity.ms%2Fcollect; _ga_DZ4MXZBLKH=GS1.1.1739872087.1.1.1739872127.20.0.0; NYK_ECOUNTER=143; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; EXP_new-relic-client=variant1; EXP_pdp-brandbook=pdp-brandbook-a; EXP_pdp-sizesection-v2=pdp-sizesection-v2; EXP_plp-quick-filters=variant1; EXP_quick-view=quick-view-visible; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~-1~YAAQTHLBF6s6QwWVAQAADX15GA190qhob3VaCmbLW0nIgJxm5LtrTla0qD/wGHjzSxX+1bEaNZcBo1je8W4WdKbhm3tQ67r9TPxClVmElhsCAPLKdKGv/VMaJdF7Tuvz9vHu4q7N9zaYG1CXuOMLO/cNnskMRs+BwF3jqDsMcgoxV6dWGsD2btvzfKa+Y0hlT9jUkFgI3Xbt5k4lEkRKKWhIgTY19cYzD3ELiP0I7tCqImK/LANh+Mwx2QfcryKOwr7L8Xig2+cKx8sL5g9OSw1vBylcwfDbM2Un4SESNmioqYZZgakZ3D7+EsXMvwBCkhp3jQJEwNS4kl7cLHI+epJtOlXFC4G/wp5LzPK2y0TI8+xNmn6z8jHCY0UKqidqpAmLkWgz3zYV31HKsEUiVS+7Rv0Zw8dJ0SgLXEKoKziotg1diwc9y7Co0zhX+9bAuo9Ae+SIXwtAVvneQTwJPDWAheDyZ35m5JpB4Bt2FzQsPyKjdP9wTE4ECYB1bLac715XI8ir/t5BvezrVIVXug2ZdvdvvVbXsu1ehfsKJA==~0~-1~1739874099; bcookie=64632cb1-b42a-4183-a718-b45b7e06a5fa',
            'domain': 'NYKAA_FASHION',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.nykaafashion.com/women/indianwear/lehengas/c/652?f=brand_filter%3D57825_',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'x-csrf-token': 'zweQmbbdgg4Cp6dE'
        }

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'pending'}, start=self.start,
                                              end=self.end)
        for result in results:
            main_category_name = result['main_category_name']
            category_id = result['category_id']
            category_name = result['category_name']
            sub_category_name = result['sub_category_name']
            sub_category_id = result['sub_category_id']
            brand_id = result['brand_id']
            brand_name = result['brand_name']
            product_count = result['product_count']
            sub_category_url = result['sub_category_url']
            hash_id = result['hash_id']
            page_count = 1

            url = (f"https://www.nykaafashion.com/rest/appapi/V2/categories/products?PageSize=50&filter_format=v2"
                   f"&apiVersion=5&currency=INR&country_code=IN&deviceType=WEBSITE&sort=popularity&device_os=desktop"
                   f"&categoryId={sub_category_id}&currentPage={page_count}&brand_filter={brand_id}")
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, dont_filter=True,
                                 meta={"main_category_name": main_category_name,
                                       'category_id': category_id,
                                       "category_name": category_name,
                                       "sub_category_name": sub_category_name,
                                       "sub_category_id": sub_category_id,
                                       "sub_category_url": sub_category_url,
                                       "page_count": page_count,
                                       "hash_id": hash_id,
                                       "url": url,
                                       "brand_id": brand_id,
                                       "brand_name": brand_name})

    def parse(self, response, **kwargs):
        main_category_name = response.meta['main_category_name']
        category_id = response.meta['category_id']
        category_name = response.meta['category_name']
        sub_category_name = response.meta['sub_category_name']
        sub_category_id = response.meta['sub_category_id']
        sub_category_url = response.meta['sub_category_url']
        old_hash_id = response.meta['hash_id']

        products_lst = ''
        json_data = ''
        try:
            json_data = json.loads(response.text)
            products_lst = json_data.get('response').get('products')
        except Exception as e:
            print(e)

        if products_lst is not None:
            for product_data in products_lst:
                item = NykaaPdpLinksItem()
                item['main_category_name'] = main_category_name
                item['category_name'] = category_name
                item['sub_category_name'] = sub_category_name
                item['sub_category_id'] = sub_category_id
                item['sku'] = product_data.get('sku')
                item['image_url'] = product_data.get('imageUrl')
                item['title'] = product_data.get('title')
                item['product_name'] = product_data.get('subTitle')
                item['product_id'] = product_data.get('id')
                item['brand'] = product_data.get('title')
                if "https://" not in product_data.get('actionUrl'):
                    item['product_url'] = "https://www.nykaafashion.com" + product_data.get('actionUrl')
                else:
                    item['product_url'] = product_data.get('actionUrl')
                item['in_stock'] = "Available" if not product_data.get('isOutOfStock') else "Not Available"
                item['images_urls'] = self.get_all_images(product_data)
                item['mrp'] = product_data.get('price')
                item['price'] = product_data.get('discountedPrice')
                item['discount'] = product_data.get('discount')
                item['size_chart'] = self.get_size_chart(product_data)
                item['colour'] = product_data.get('sibling_colour_codes') if product_data.get(
                    'sibling_colour_codes') else "NA"
                item['tags'] = " | ".join([i.get('title') for i in product_data.get('tag', [])])
                if not item['tags']:
                    item['tags'] = "NA"
                item['hash_id'] = str(
                    int(hashlib.md5(bytes(
                        str(item['main_category_name']) + str(item['category_name']) + str(
                            item['sub_category_name']) + str(
                            item['product_id']), "utf8")).hexdigest(),
                        16) % (
                            10 ** 10))
                yield item

            if response.status in self.handle_httpstatus_list:
                return

            # Todo: Pagination
            if products_lst:
                page_count = response.meta.get('page_count') + 1
                brand_id = response.meta.get('brand_id')
                brand_name = response.meta.get('brand_name')
                print("Page count: ", page_count)

                url = (f"https://www.nykaafashion.com/rest/appapi/V2/categories/products?PageSize=50&filter_format=v2"
                       f"&apiVersion=5&currency=INR&country_code=IN&deviceType=WEBSITE&sort=popularity&device_os=desktop"
                       f"&categoryId={sub_category_id}&currentPage={page_count}&brand_filter={brand_id}")
                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, dont_filter=True,
                                     meta={"main_category_name": main_category_name,
                                           'category_id': category_id,
                                           "category_name": category_name,
                                           "sub_category_name": sub_category_name,
                                           "sub_category_id": sub_category_id,
                                           "sub_category_url": sub_category_url,
                                           "page_count": page_count,
                                           "hash_id": old_hash_id,
                                           "url": url,
                                           "brand_id": brand_id,
                                           "brand_name": brand_name})
            else:
                mycursor = conn.cursor()
                # sql = f"UPDATE new_category_links SET status = 'Done' WHERE hash_id = {old_hash_id}"
                sql = f"UPDATE new_category_links_with_brand_id SET status = 'Done' WHERE hash_id = {old_hash_id}"
                mycursor.execute(sql)
                conn.commit()


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {NykaaPdpLinksSpider.name} -a start=1 -a end=100000".split())

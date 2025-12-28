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
    name = "pdp_links"
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
        self.db = ConfigDatabase(database="nykaa_fashion", table='new_category_links')  # cat_links
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'bcookie=069a8da2-143f-49f8-bf13-b830e8ebaf52; EXP_plp-quick-filters=variant1; EXP_new-relic-client=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; tm_stmp=1739601680788; rum_abMwebSort=17; _gcl_au=1.1.895711510.1739601681; PHPSESSID=a5d4d24d2efd42e99df2a975736bb370; _ga=GA1.1.549537741.1739601681; WZRK_G=b610c16de4184b62bfd4dc5adcb00b20; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; EXP_SSR_CACHE=182338fc37e6d3e8a85abbd1a1dd2b09; form_key=yowgtTva1RLcSUPU; AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg=-1303530583%7CMCIDTS%7C20135%7CMCMID%7C18915836392668149223411254796099779152%7CMCAAMLH-1740206843%7C12%7CMCAAMB-1740206843%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1739609243s%7CNONE%7CvVersion%7C3.3.0; __stp=eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiI2Njk3YjE4NS0yNTgxLTQ1MmItYmZhMi0zOTY5NzA0ZjhmN2UifQ==; NYK_VISIT=069a8da2-143f-49f8-bf13-b830e8ebaf52~1739775016341; _clck=1jzunvf%7C2%7Cfti%7C0%7C1870; _clsk=wy7lt1%7C1739775665656%7C9%7C1%7Ch.clarity.ms%2Fcollect; bm_sz=B7DC41C5901A9052082BF16299F0EF76~YAAQTXLBF9z3SeKUAQAA3ee3EhooJlbRi+PMaqyuMR6bA6rdpZeE5jCkE4tiv3xGtGKTI2QnzPqM65C8SP05N9ZQAnnPzqLxLaFV5jV+C+3FUrsWFDkGYAgny46ufbO61holgLvSxL4KC8gGQNx093gR40mhlhpdISol1CoybkdYRoXPNzycMqbV5HpJByqJG74tsfeEDawYNjOr+yccZFDR2zrXaheWXEL3OMpfPnqhUWvy3Lx8vFS1gF7WEhf1EdmWMGcm9Y5LVCyJ57bp/iPrdtZCQ4Xk3rvP6dokk0EAMPfrjkh1ftY4ZLn6EVivm1Pj3XFR2IaxcIwzJ36D83GEvQ3Myt7Wj8hwEyMrPFDHFkJscKQ2mDqOODi0lAXy4kLtbMw6hWnoPW+aEsnn50fmgFXavtMbu+9KVOuKtVaSPxKElxp7UnCvy5QGhvTKy5VnD+VmU0ud4A8LWKZAI5z+o8LgsK00rDbZyjPl~3293495~3683141; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A8%2C%22s%22%3A1739775157%2C%22t%22%3A1739775664%7D; _ga_DZ4MXZBLKH=GS1.1.1739775020.4.1.1739775676.28.0.0; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQTXLBF3D7SeKUAQAA1Ae4Eg1Hm+JvN5gPqWkELhbtNbKa8aYzMwS23wOSAk2a8r3eB2IBUzPPOfA0pzJjqW8wnAHZ7Zf1fu6e0Hrji8FrGuQ0v8tpRUWGnDPKRDCR9ElfE9u0Gdsy4SZYniwLAuk+y3DvItReoEPqpCfRPoJO9I4BwLp/8h0Me2OEEASqxAgz0iPGZQczejU5HSwC7GHFFy29GgHKP5Yi6twmRlR/5ZA+IYD8Pk0XPrrwwCfIj+J3dpMNeYXuUkLbjHd1Uat4pNHtyS4dwq0Nvz0pbdAnvcm16klF5nPreSIBtGONHcqGdbQG8y53G/QOUpOWiFZ0D7Gm5SInAL/4si1g21EadUJTcZ9UuyH40jGIJoZk6GypGy241enjWOWgkyR6cBz3ADBm9Rs3wt5jBKXeSo0sERJd9q+psl1ue9KZVnjUOIKwPw/Htwnm0H+harz+svpUZUqJ6QquJF2BcGLIXdfou7IW8NLfK65uchjffc1cHOzq8+ddwihV6lcH2scFKZP/B8GWLJDBHMNr93/+Jg==~-1~-1~1739778739; NYK_PCOUNTER=8; NYK_ECOUNTER=465',
            'domain': 'NYKAA_FASHION',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.nykaafashion.com/men/topwear/t-shirts/c/6825?root=nav_3&ptype=listing%2Cmen%2Ctopwear%2Ct-shirts%2C4%2Ct-shirts&p=2',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'x-csrf-token': 'yowgtTva1RLcSUPU',
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
            sub_category_url = result['sub_category_url']
            hash_id = result['hash_id']
            page_count = 1
            url = (f"https://www.nykaafashion.com/rest/appapi/V2/categories/products?PageSize=50&filter_format=v2"
                   f"&apiVersion=5&currency=INR&country_code=IN&deviceType=WEBSITE&sort=popularity&device_os=desktop"
                   f"&categoryId={sub_category_id}&currentPage={page_count}")
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, dont_filter=True,
                                 meta={"main_category_name": main_category_name,
                                       'category_id': category_id,
                                       "category_name": category_name,
                                       "sub_category_name": sub_category_name,
                                       "sub_category_id": sub_category_id,
                                       "sub_category_url": sub_category_url,
                                       "page_count": page_count,
                                       "hash_id": hash_id,
                                       "url": url})

    def parse(self, response, **kwargs):
        global json_data
        main_category_name = response.meta['main_category_name']
        category_id = response.meta['category_id']
        category_name = response.meta['category_name']
        sub_category_name = response.meta['sub_category_name']
        sub_category_id = response.meta['sub_category_id']
        sub_category_url = response.meta['sub_category_url']
        old_hash_id = response.meta['hash_id']

        products_lst = ''
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
                mycursor = conn.cursor()
                sql = f"UPDATE new_category_links SET status = '{response.status}' WHERE hash_id = {old_hash_id}"
                mycursor.execute(sql)
                conn.commit()

            # Todo: Pagination
            if products_lst:
                page_count = response.meta.get('page_count') + 1
                print("Page count: ", page_count)
                url = (f"https://www.nykaafashion.com/rest/appapi/V2/categories/products?PageSize=50&filter_format=v2"
                       f"&apiVersion=5&currency=INR&country_code=IN&deviceType=WEBSITE&sort=popularity&device_os=desktop"
                       f"&categoryId={sub_category_id}&currentPage={page_count}")
                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse, dont_filter=True,
                                     meta={"main_category_name": main_category_name,
                                           "category_id": category_id,
                                           "category_name": category_name,
                                           "sub_category_name": sub_category_name,
                                           "sub_category_id": sub_category_id,
                                           "sub_category_url": sub_category_url,
                                           "page_count": page_count,
                                           "hash_id": old_hash_id,
                                           "url": url})
            else:
                mycursor = conn.cursor()
                sql = f"UPDATE new_category_links SET status = 'Done' WHERE hash_id = {old_hash_id}"
                mycursor.execute(sql)
                conn.commit()


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {NykaaPdpLinksSpider.name} -a start=21 -a end=21".split())

import re
from turtledemo.penrose import start
from typing import Iterable, Any

import pymysql
import scrapy

from scrapy import cmdline
from amazon_seller.config.database_config import ConfigDatabase
import amazon_seller.config.db_config as db_config


def get_seller_feedback(seller_name):
    if "Cocoblu Retail".lower() in seller_name.lower():
        return "93"
    elif "siril" in seller_name.lower():
        return "99"
    elif "AARSH LIFESTYLE".lower() in seller_name.lower():
        return "89"
    elif "Mirchi Fashion".lower() in seller_name.lower():
        return "96"
    elif "Pujia Mills®".lower() in seller_name.lower():
        return "75"
    elif "PANDADI SAREE".lower() in seller_name.lower():
        return "46"
    elif "JMM India".lower() in seller_name.lower():
        return "91"
    else:
        return "0"


class GetProductDataSpider(scrapy.Spider):
    name = "get_product_data"
    allowed_domains = ["www.amazon.com"]

    # start_urls = ["https://www.amazon.com"]

    def __init__(self, start_index, end, **kwargs):
        super().__init__()
        self.cookies = {
            'session-id': '257-8197099-3389816',
            'i18n-prefs': 'INR',
            'lc-acbin': 'en_IN',
            'ubid-acbin': '261-8449377-2614061',
            'session-token': 'okvZ0QGEZYqql3XejHiCjpCvqh6IeESm3l1N48IFot3tP5AoHs6pG0IUs7ewjGDr9GYfTMZVGD2jyxCeoKSBqt5OsFeMTGXIbnmcOrfniU+Q2WSsgPCMoRkyRjPFJ0Zz2ABUCdrawUwJGtRrwqiNhAf4tM3wLxK6iTXMb9Ln4+5wEsi3HtI69MvvaqV5kudbxPWFEckm2ovZJpq8BwzTcjiUlixMU8qnleP99d+h5Po8mX0gIU8x0SE5iALWAdGK+yk1AbrYlqGZ3jBPQPleoHRDvCDVthD2XEF1dODuKFgNV+AJqXZod5l4fzN8Vx4lMQKSwMi/a2mmFvOOCcOAXmW4ZsztTlbG',
            'csm-hit': 'tb:QHBFKPGTWM38JB2DDZA5+s-FCNQZGH98614AK80RXG2|1752942447280&t:1752942447280&adb:adblk_no',
            'session-id-time': '2082787201l',
            'rxc': 'AKsPUdhIcyPXiy9gFbM',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'device-memory': '8',
            'downlink': '4.95',
            'dpr': '1',
            'ect': '4g',
            'priority': 'u=0, i',
            'rtt': '250',
            'sec-ch-device-memory': '8',
            'sec-ch-dpr': '1',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-ch-viewport-width': '1920',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'viewport-width': '1920',
            # 'cookie': 'session-id=257-8197099-3389816; i18n-prefs=INR; lc-acbin=en_IN; ubid-acbin=261-8449377-2614061; session-token=okvZ0QGEZYqql3XejHiCjpCvqh6IeESm3l1N48IFot3tP5AoHs6pG0IUs7ewjGDr9GYfTMZVGD2jyxCeoKSBqt5OsFeMTGXIbnmcOrfniU+Q2WSsgPCMoRkyRjPFJ0Zz2ABUCdrawUwJGtRrwqiNhAf4tM3wLxK6iTXMb9Ln4+5wEsi3HtI69MvvaqV5kudbxPWFEckm2ovZJpq8BwzTcjiUlixMU8qnleP99d+h5Po8mX0gIU8x0SE5iALWAdGK+yk1AbrYlqGZ3jBPQPleoHRDvCDVthD2XEF1dODuKFgNV+AJqXZod5l4fzN8Vx4lMQKSwMi/a2mmFvOOCcOAXmW4ZsztTlbG; csm-hit=tb:QHBFKPGTWM38JB2DDZA5+s-FCNQZGH98614AK80RXG2|1752942447280&t:1752942447280&adb:adblk_no; session-id-time=2082787201l; rxc=AKsPUdhIcyPXiy9gFbM',
        }
        self.start_index = start_index
        self.end = end
        self.variation_id_table = ConfigDatabase(table=db_config.variation_id_table,
                                                 database=db_config.database_name)
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="actowiz",
            database=db_config.database_name
        )

    def start_requests(self):
        results = self.variation_id_table.fetchResultsfromSql(conditions={'status': 'Pending'}, start=self.start_index,
                                                              end=self.end)
        for result in results:
            item_type = result['item_type']
            parent_pid = result['parent_pid']
            child_pid = result['child_pid']
            sr_nos_1 = result['sr_nos_1']
            sr_nos_2 = result['sr_nos_2']

            url = f"https://www.amazon.in/dp/{child_pid}"
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies,
                                 meta={"item_type": item_type,
                                       "parent_pid": parent_pid, "child_pid": child_pid, "sr_nos_1": sr_nos_1,
                                       "sr_nos_2": sr_nos_2},
                                 dont_filter=True)

    def parse(self, response, **kwargs):
        product_type = response.meta.get('item_type')
        parent_pid = response.meta.get('parent_pid')
        child_pid = response.meta.get('child_pid')
        sr_nos_1 = response.meta.get('sr_nos_1')
        sr_nos_2 = response.meta.get('sr_nos_2')

        # Todo: asin_no
        try:
            asin_no = child_pid
        except:
            asin_no = "N/A"

        # Todo: amazon_fulfilled
        try:
            if response.xpath('//div[@data-feature-name="shippingMessageInsideBuyBox"]//*[@aria-label="Fulfilled"]'):
                amazon_fulfilled = True
            else:
                amazon_fulfilled = False
        except Exception as e:
            print(e)

        # Todo: seller_name
        try:
            seller_name = response.xpath("//span[@id='productTitle']/text()").get('').strip()
        except:
            seller_name = "N/A"

        # Todo: Product Rating
        try:
            product_rating = response.xpath("//*[@id='acrPopover']/@title").get()
            # pattern = "(.*)out of 5 stars"
            # match = re.search(pattern, product_rating)
            # if match:
            #     rating = match.group(1).strip()
            # else:
            #     rating = "N/A"
        except:
            product_rating = 'N/A'

        # todo: product total rating
        try:
            no_of_rating_list = response.xpath("//*[@id='acrCustomerReviewText']/text()").getall()
            no_of_rating_lst = "".join(list(set(no_of_rating_list)))
            no_of_rating = no_of_rating_lst.replace(",", "").replace("ratings", "").strip()
        except:
            no_of_rating = "N/A"

        # Todo: seller_feedback
        try:
            seller_name = response.xpath(
                "//span[contains(text(),'Sold by')]/../../following-sibling::div//a/text()").get()
            seller_feedback = get_seller_feedback(seller_name)
        except:
            seller_feedback = "N/A"

        # Todo: item_link
        try:
            item_link = response.url
        except:
            item_link = "N/A"

        # Todo: price
        try:
            price = response.xpath(
                "//div[@class='a-section a-spacing-none aok-align-center aok-relative']//span[@class='a-price-whole']/text()").get()
        except:
            price = "N/A"

        # Todo: Item Name
        try:
            item_lst = []
            item_name_list = response.xpath("//h1[@id='title']//text() | //span[@id='productTitle']//text()").getall()
            for item in item_name_list:
                if item:
                    item_lst.append(item.strip())
            item_name = "".join(item_lst)
        except:
            item_name = 'N/A'

        # Todo: Brand Name
        try:
            brand_name = response.xpath("//a[@id='bylineInfo']/text() | //a[contains(text(),'Brand')]/text()").get()
            if brand_name:
                brand_name = brand_name.replace("Brand:", "").strip()
        except:
            brand_name = "N/A"

        # Todo: about_this_item
        try:
            about_this_list = []
            about_this_dict = {}
            li_list = response.xpath('//*[contains(text(),"About this item")]//parent::div[@id="feature-bullets"]//li')
            if not li_list:
                li_list = response.xpath('//*[contains(text(),"About this item")]//parent::div//li')
            if not li_list:
                li_list = response.xpath('//div[@id="feature-bullets"]//li')
            for li in li_list:
                li_text = li.xpath(".//text()").get('').strip()
                if li_text:
                    about_this_list.append(li_text)
            if about_this_list:
                for index, item in enumerate(about_this_list, start=1):
                    about_this_dict[f'Bullet Point - {index}'] = item
            print(about_this_dict)
        except:
            about_this_item = "N/A"

        # Todo: target gender
        try:
            if isinstance(item_name, str):
                if "women" in item_name.lower():
                    target_gender = "Women"
                elif "men" in item_name.lower():
                    target_gender = "Men"
        except:
            target_gender = "N/A"

        # Todo:product details
        try:
            product_detail = dict()
            key_list =response.xpath("//*[@id='detailBullets_feature_div']//li//span[@class='a-text-bold']/text()")
            value_list = response.xpath("//*[@id='detailBullets_feature_div']//li//span[@class='a-text-bold']/following-sibling::span/text()").getall()

            # for detail in response.xpath('//*[@id="detailBullets_feature_div"]//li'):
            #     key_list = [re.sub(r'[\n\u200f\u200e]+', '', i).strip() for i in
            #            detail.xpath('.//span[@class="a-text-bold"]/text()').getall() if i.strip()]
            #     key = "".join(key_list).strip()
            #     key = key.replace(":", "").strip()
            #     value_list = detail.xpath('./span[@class="a-text-bold"]/following-sibling::span/text()')
            #     if key and value:
            #         product_detail[key] = value
        except:
            ''


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {GetProductDataSpider.name} -a start_index=1 -a end=5".split())

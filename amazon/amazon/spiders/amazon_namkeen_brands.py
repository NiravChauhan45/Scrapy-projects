import json
import math
import os
from datetime import datetime

import numpy as np
import pandas as pd
import requests
import scrapy
from scrapy import cmdline, Selector


class AmazonNamkeenBrandsSpider(scrapy.Spider):
    name = "amazon_namkeen_brands"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'device-memory': '8',
            'downlink': '10',
            'dpr': '1.2000000000000002',
            'ect': '4g',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://www.amazon.in/s?k=namkeen',
            'rtt': '50',
            'sec-ch-device-memory': '8',
            'sec-ch-dpr': '1.2000000000000002',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-ch-viewport-width': '1600',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'viewport-width': '1600',
            'Cookie': 'i18n-prefs=INR; session-id=262-7090653-5372514; session-id-time=2082787201l; session-token=XVcSvPwVnWKMD/xWL+l/eztVj7NROWNLvRQtW37xGM/bpbYZwoG4rrmqtJ56paAvS0YsbEuHDvsr/NeVPpAYkyc5YLXdKKFdYNIwPQmbE4gP6cs2FAhv+pThIdni+RgYNzC3e6LLdxmzRVt9PYt/oRwcqhbFLwUt9Bnhkvfw3fAQqS1RimrwYP7Q6qTsCXPx7uROdDUlcG0a/Td9mHSUIRofr2MslMJxuapN0iT6YP/hWJBNaNx589fOu4fM0KpLWm0RdTjzg95uH/LmePd5lzylVKosTR1OsclqoRNcAdsHP//THKZJuDfxizDeWUpXZVg0LfBbdXeAM8kQM6khGujJUE3a8Joh; ubid-acbin=259-9378471-4704661'
        }
        self.current_date = datetime.now().strftime("%d_%m_%Y")
        self.main_df = []
        self.main_df_dict = {}
        self.filepath = f"..\output_files"
        self.filename = f"Amazon_namkeen_{self.current_date}_brands.xlsx"
        os.makedirs(self.filepath, exist_ok=True)

    handle_httpstatus_list = [500, 503]

    def start_requests(self):
        brand_url_list = [
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A66259&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_1&ds=v1%3ABY8YqeR9FSYyPETbM774iA8kfMO2GkwDJ%2BsO0FmS40o",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A209664&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_2&ds=v1%3AyPRg79Trj1pUDfh61vFv2Z69pBoCUfxN4ySt1BYr8mk",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A683680&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_3&ds=v1%3AKcpeccp2D5l3PLDhRLHE6aab2PO9igmaK7aO5kp07dU",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A851718&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_4&ds=v1%3AX7FqknE7fN62AiT%2BGrwH1SyG2FwXYH8%2B%2B9jRCjtKkFA",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A2049756&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_5&ds=v1%3AwPOJRFNb1SMVpVT6QDuHBIvyyimPnqqMqex%2BzXf0%2BQ8",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A363738&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_6&ds=v1%3AoOkEhjY7WrJZwn%2FM6xEvCdmstvpIhJfBfo7lJUPrSrk",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A541709&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_7&ds=v1%3A1%2FmO6rrecDPoL9c%2BXMjy%2BEuTR4UK3bhHs313tJ3yVMI",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A569034&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_8&ds=v1%3AHkTChTUXPzufKd1UWPhooxqqAvQTEDU46K%2FVLjsf%2Bx4",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A581403&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_9&ds=v1%3AzF9UWuh2w1JLo%2BEMGH00dqixyHZ5ofrDZTBKVoFkjXc",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A691294&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_10&ds=v1%3AhUpZ%2BJOGbW0U%2BksbCAf2SUMXWiqix5%2F0%2Fp2nBjGLx4g"
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A804989&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_11&ds=v1%3ARqwP7NSJgD4dQkmkj%2Fgmf%2F4lKpQ9zOP8Jv21TU2JJRk"
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A666805&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_12&ds=v1%3ASWWKvvkFdjrZKg09ZQnJ4HB99TmZdiVpA%2BgRhhcvd6Y",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A448690&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_13&ds=v1%3AIGgzZM90D1zD2ps7dfqzmEVn3uigucIJoK1rDinBD6Y",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A715841&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_14&ds=v1%3AfGL7kKc5SNSj6B7mhPJzh%2F14nb4dXmk4sfIvKfiSy3Y",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A679497&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_15&ds=v1%3A0wWWH1IYUzHDAnzwzlc5d7ok7dyslhCurpuu0YffwWE",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A515248&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_16&ds=v1%3AQzClqC%2FTeo7JhMWl5wnOWgn5vfYrCVFCG7dmZUubDBI",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A1287545&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_17&ds=v1%3AIbuj4nNGX8mej%2BejV6CUjy9gIkOAxONAUDw1MkIDsKU",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A1311799&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_18&ds=v1%3A3gYihL3EBkMRW3TpZGTaeBarnj5Tv0L6vU8vKKu1IYo",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A1458656&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_19&ds=v1%3AbEIpCOGmyjKjuEkOMRynU0jEyit2RSiP%2FpqOdZLbrsk",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A380107&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_20&ds=v1%3AOoISuSMNbpINz9%2BP05kdpc24YMRI3fdyQhsmVYVqmk4",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A1880549&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_21&ds=v1%3AVFruUnXOKN1u7%2BtUBxeNngt1g37JRKyUJrpZoELhl1s",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A372653&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_22&ds=v1%3A2teG%2FPHAIyCQv9djA2GasrxWtXeZk2%2F54bw0Ug29YhU",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A729336&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_23&ds=v1%3ATl55Olju05Y%2BIi2oH%2BNrc4jcCF2kUFSTSr%2Bwt1e8kP4",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A1238849&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_24&ds=v1%3A2GP43KRHl9Vlypr6Nj%2BF2CNsCd9L2Cc7r3h0scn4Y7U",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A416528&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_25&ds=v1%3A0ePZ%2BkM5JI5xGepnT1CvW6oF7pUDqXsD5flfvl0Ye%2F0",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A546460&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_26&ds=v1%3AmfldToVyLx7jWj8Z63HDcBT9gwYopgD9wqtWQZcSeKE",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A476279&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_27&ds=v1%3A5Ec%2BASMFQ8e9BbwpJjQqMHIOVo%2FpAEUz7UnwXF0uIZ8",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A592897&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_28&ds=v1%3AIT7tWUawzRHCs1EcGaU67HnbLuaE1mMWe1aR9bWi9eo",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_123%3A95467&dc&qid=1740124039&rnid=91049095031&ref=sr_nr_p_123_29&ds=v1%3A8jrBmxQrX5Dbwjhzcmcs1EMsTtidnImNZY4u%2BpZeBZ4"
        ]
        for brand_url in brand_url_list:
            url = "https://www.amazon.in" + brand_url
            response = requests.get(url, headers=self.headers)
            yield scrapy.Request(url="https://example.com", meta={"selector": Selector(text=response.text)},
                                 callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        selector = response.meta.get('selector')
        discount_id = response.meta.get('discount_id')
        product_data_lst = selector.xpath("//div[@role='listitem']")
        for index, product_data in enumerate(product_data_lst):
            if product_data.xpath(".//div[@data-cy='title-recipe']/a/@href").get():
                product_link = product_data.xpath(".//div[@data-cy='title-recipe']/a/@href").get()
                product_id = ''
                if '/sspa/click?ie' not in product_link:
                    product_id = product_link.split("/dp/")[-1].split('/ref')[0]
                else:
                    product_id = product_data.xpath("./@data-asin").get('').strip()
                product_name = product_data.xpath(".//div[@data-cy='title-recipe']/a/h2//text()").get('').strip()
                brand = 'N/A'
                try:
                    price = product_data.xpath(
                        './/div[contains(@class,"s-price-instructions-style")]//span[@class="a-price"]//span[@class="a-offscreen"]/text()').get().replace(
                        '₹', '')
                except:
                    price = 'N/A'
                try:
                    mrp = product_data.xpath(
                        ".//div[contains(@class,'s-price-instructions-style')]//div[@class='a-section aok-inline-block']//span[@class='a-offscreen']/text()").get().replace(
                        '₹', '')
                except:
                    mrp = price
                try:
                    discount_percentage = ((int(mrp) - int(price)) / int(mrp)) * 100 if mrp or price else "N/A"
                    discount_percentage = "N/A" if round(discount_percentage, 2) == 0.0 else math.ceil(
                        discount_percentage)
                except:
                    discount_percentage = 'N/A'

                in_stock = "TRUE" if price else "FALSE"

                tag1 = product_data.xpath(
                    './/div[@class="a-row a-color-base"]//span[contains(@class,"a-size-base a-color-base s-background-color-platinum")]/text()').get()
                tag2 = product_data.xpath(".//i[@aria-label='Amazon Prime']/@aria-label").get()
                tag3 = product_data.xpath('.//div[@data-cy="price-recipe"]//span[@class="a-badge-text"]/text()').get()
                tag = [i for i in [tag1, tag2, tag3] if i]

                image = product_data.xpath(".//img[@class='s-image']/@src").get('').strip()
                avg_rating = \
                    product_data.xpath(".//i[@data-cy='reviews-ratings-slot']//text()").get('').split('out of')[
                        0].strip()
                number_of_rating = product_data.xpath(".//span[@class='a-size-base s-underline-text']/text()").get(
                    '').strip()
                self.main_df_dict = {
                    'product_id': product_id,
                    'product_name': product_name,
                    'brand': brand,
                    'mrp': mrp,
                    'price': price,
                    'discount': discount_percentage,
                    'in_stock': in_stock,
                    'tag': tag,
                    'image': image,
                    'avg_rating': avg_rating,
                    'number_of_rating': number_of_rating.replace(',', '')
                }
                # print(json.dumps(self.main_df_dict))
            self.main_df.append(self.main_df_dict)
        next_page = selector.xpath("//a[contains(text(),'Next')]/@href").get()
        if next_page:
            next_page_url = "https://www.amazon.in" + next_page
            response = requests.get(next_page_url, headers=self.headers)
            yield scrapy.Request(url="https://example.com", meta={"selector": Selector(text=response.text)},
                                 callback=self.parse, dont_filter=True)

    def close(self, reason):
        if self.main_df:
            try:
                os.makedirs(self.filepath, exist_ok=True)  # Todo: create a folder if not exits
                df = pd.DataFrame(self.main_df)  # .sort_values(by='Id')
                df.replace(np.NaN, 'N/A', inplace=True)
                df.replace('', 'N/A', inplace=True)
                df = df.drop_duplicates()
                df.to_excel(f'{self.filepath}\\{self.filename}', index=False)
                self.log(f"Data saved to {self.filename} because {reason}")
            except Exception as e:
                print(e)
        else:
            print("No Data Found !!")


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {AmazonNamkeenBrandsSpider.name}".split())

import json
import math
import os
from datetime import datetime

import numpy as np
import pandas as pd
import requests
import scrapy
from scrapy import cmdline, Selector


class AmazonNamkeenSellerSpider(scrapy.Spider):
    name = "amazon_namkeen_seller"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'device-memory': '8',
            'downlink': '1.4',
            'dpr': '1.2000000000000002',
            'ect': '3g',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://www.amazon.in/s?k=namkeen',
            'rtt': '350',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'viewport-width': '1600',
            'cookie': 'session-id=257-7531149-4556969; i18n-prefs=INR; ubid-acbin=257-6780858-2677716; session-token=rvqHN45qGl7Akatj89jouoZIiVbSUQKh9QVYDA2m1NN2c+Ta01SmKZzqymDjgGndVGT8XZBkdS3576Pz/1x9xnH2c8bzasyHWttQjVY83j6nHCl1Fimxt3/uP+GgHPZKniDO7WKseM0T+gs7FaZ4eWLItEhGs9u/D5aNmM5cHWFH7zIm8+x6IUdfYW4XgrpLh1Mm1D17ZV6dyOTCzU6mVw6Ce7vUrjss+wR7BYqL/UUNFqjrYfkpllKT7dabdQihZI2MBOl7iz7QMepQ0ArvuwoPf/GUtZ3XiKbGSeQINW0PXp1VBVXMdVzHSt4roybrTO9s61u/T5XJub3msNZbX8Yu7j6mkSw+; csm-hit=tb:RA05DJF8JGZBZ05NV3RQ+s-Y1XV9RX1MA59BGK2H263|1740126919888&t:1740126919888&adb:adblk_no; session-id-time=2082787201l',
        }
        self.current_date = datetime.now().strftime("%d_%m_%Y")
        self.main_df = []
        self.main_df_dict = {}
        self.filepath = f"..\output_files"
        self.filename = f"Amazon_namkeen_{self.current_date}_seller_2_to_6.xlsx"
        os.makedirs(self.filepath, exist_ok=True)

    handle_httpstatus_list = [500, 503]

    def start_requests(self):
        seller_url_list = [
            # "/s?k=namkeen&rh=n%3A2454178031%2Cp_6%3AA2Y8B21I81HLOR&dc&qid=1740126435&rnid=1318474031&ref=sr_nr_p_6_1&ds=v1%3AdQRHXQo%2BRh10TBorBdz6KjrcOiPc%2FW%2BeIwoFj5fJsDY",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_6%3AA2I7QBETQOH9F1&dc&qid=1740126435&rnid=1318474031&ref=sr_nr_p_6_2&ds=v1%3Ae93VrgkjyIWuNW0CjmUKcNn%2BUnr55sAkbFv1qrs%2FP9Y",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_6%3AA2QVB0R72LAC7N&dc&qid=1740126435&rnid=1318474031&ref=sr_nr_p_6_3&ds=v1%3AGh0d%2BeqSEi96IHl2OKxIzoUzMZXgLYb7aZKNaUzsAlI",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_6%3AA1WP70CVW4AY9Q&dc&qid=1740126435&rnid=1318474031&ref=sr_nr_p_6_4&ds=v1%3AeP4KINkRgFpSkbiV3alD%2FXZy%2B2S36LhVTxCTraY1ChI",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_6%3AA1083M9V765C85&dc&qid=1740126435&rnid=1318474031&ref=sr_nr_p_6_5&ds=v1%3A9K5gGIlvQD%2FD9AXaQShSCIqLYPJmwhVcdeqmPIblQs4",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_6%3AAG3IPA1X5JWTK&dc&qid=1740126435&rnid=1318474031&ref=sr_nr_p_6_6&ds=v1%3A0Ws%2FyXZD10K8qB4P6Aui1D3Z35EZbYLpHN%2Fx8%2B3bido",
            "/s?k=namkeen&rh=n%3A2454178031%2Cp_6%3AANDFJZB3VFTDD&dc&qid=1740126435&rnid=1318474031&ref=sr_nr_p_6_7&ds=v1%3A93aHQmfFrHZHfEqdn1EOrSwNIvmk3LYBjUAOxDPDjOs"
        ]

        for seller_url in seller_url_list:
            url = "https://www.amazon.in" + seller_url
            response = requests.get(url, headers=self.headers)
            yield scrapy.Request(url="https://example.com", meta={"selector": Selector(text=response.text), "url": url},
                                 callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        selector = response.meta.get('selector')

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
                print(json.dumps(self.main_df_dict))
            self.main_df.append(self.main_df_dict)
        next_page = selector.xpath("//a[contains(text(),'Next')]/@href").get()
        # page_count =
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
    cmdline.execute(f"scrapy crawl {AmazonNamkeenSellerSpider.name}".split())

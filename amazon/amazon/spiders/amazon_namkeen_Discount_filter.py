import json
import math
import os
from datetime import datetime
from typing import Iterable

import numpy as np
import pandas as pd
import scrapy
from scrapy import Request, cmdline


class AmazonNamkeenSpider(scrapy.Spider):
    name = "amazon_namkeen_discount"

    # allowed_domains = ["www.amazon.com"]
    # start_urls = ["https://www.amazon.com"]
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
            'rtt': '100',
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
            'Cookie': 'i18n-prefs=INR; session-id=262-7090653-5372514; session-id-time=2082787201l; session-token=IaXY966P6gMqyT8MTHHUYjNQcBJQ8FP7E/X++Vjvvyd0VzZKM2RfC8GeGnBTJAPj9JnEFRDYjzXg7hTFivMeiNuuWzNe6s3WEeevXEe8TvXcZLH2fFbc22aM48jPBaVBqDeEkvvxQm2IbcTGfmVXdomO9tV+tlqctjaEMg+AlxJNFCUwBGE59oqtujdikwCB8cmIfXNT8I3kGuUVdsqx9bQt2oMSompw1kD6Hdo7MlYLXtApeFyXI00VjeuI68FvnTCSgejMtkLtrhWlMP2sR+ShZl+3JmpVs78vSaTdStxbi4D7xVHXGuQs4i6bPR1F+NccE6xOXfI/tWIvj81dsNjWEjdNbbT0; ubid-acbin=259-9378471-4704661'
        }
        self.current_date = datetime.now().strftime("%d_%m_%Y")
        self.main_df = []
        self.main_df_dict = {}
        self.filepath = f"..\output_files"
        self.filename = f"Amazon_namkeen_{self.current_date}_Discount.xlsx"
        os.makedirs(self.filepath, exist_ok=True)

    def start_requests(self):
        discount_list = ["sr_nr_p_n_pct-off-with-tax_1", "sr_nr_p_n_pct-off-with-tax_2", "sr_nr_p_n_pct-off-with-tax_3",
                         "sr_nr_p_n_pct-off-with-tax_4", "sr_nr_p_n_pct-off-with-tax_5", "sr_nr_p_n_pct-off-with-tax_6"]
        for discount_id in discount_list:
            if discount_id == "sr_nr_p_n_pct-off-with-tax_1":
                url = (f"https://www.amazon.in/s?k=namkeen&rh=n%3A2454178031%2Cp_n_pct-off-with-tax%3A2665399031&dc&ds"
                       f"=v1%3AAtYqG2cVPkPuX1CoL%2F4bSAGCpSmty16%2BDcGG4C2FT5E&crid=3C0PDQNKPQV67&qid=1740122094&rnid"
                       f"=2665398031&sprefix=namkeen%2Caps%2C230&ref={discount_id}")
                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse,
                                     meta={'discount_id': discount_id}, dont_filter=True)
            else:
                url = (f"https://www.amazon.in/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_pct-off-with-tax"
                       f"%3A2665402031&dc&ds=v1%3ATrxHV3LjAd9yV0ByxsTstvzgiXB33qLTjAjuATZoBcc&crid=3C0PDQNKPQV67&qid"
                       f"=1740122202&rnid=2665398031&sprefix=namkeen%2Caps%2C230&ref={discount_id}")
                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse,
                                     meta={'discount_id': discount_id}, dont_filter=True)

    def parse(self, response, **kwargs):
        discount_id = response.meta.get('discount_id')
        product_data_lst = response.xpath("//div[@role='listitem']")
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
        next_page = response.xpath("//a[contains(text(),'Next')]/@href").get()
        if next_page:
            next_page_url = "https://www.amazon.in" + next_page
            next_page_url = next_page_url.split('&ref=')[0] + f"&ref={discount_id}"
            yield scrapy.Request(url=next_page_url, headers=self.headers, callback=self.parse, dont_filter=True)

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
    cmdline.execute(f"scrapy crawl {AmazonNamkeenSpider.name}".split())

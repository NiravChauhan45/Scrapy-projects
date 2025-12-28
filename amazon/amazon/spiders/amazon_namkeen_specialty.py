import json
import math
import os
from datetime import datetime

import numpy as np
import pandas as pd
import requests
import scrapy
from scrapy import Selector, cmdline


class AmazonNamkeenSpecialtySpider(scrapy.Spider):
    name = "amazon_namkeen_specialty"
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
        self.filename = f"Amazon_namkeen_{self.current_date}_specialty.xlsx"
        os.makedirs(self.filepath, exist_ok=True)

    handle_httpstatus_list = [500, 503]

    def start_requests(self):
        speciality_url_list = [
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868021031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_1&ds=v1%3A3A%2Bhf9%2FudFuGF%2BTVAH6TkdvXqLAFkignqtWJP1Japvo",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868023031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_2&ds=v1%3ALQ944ol%2BjdHtHn4FYpGjfpQjkAV0i72J5Zp%2BHueCbVg",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868025031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_3&ds=v1%3A2fpOQ9OD4lqfhy0MLJ3%2F4GKUnEsgH5%2BvBoBdytkEH68",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868033031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_4&ds=v1%3ApJmezpikubo3rQh70%2F8dac9VuON6z%2FH5XtoplI92kDg",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868038031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_5&ds=v1%3A5NDxKa9q%2FBP7efDffdRNVK5%2BONldAse0P8QZorOHc%2FA",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868039031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_6&ds=v1%3ATyDKRfz1lLNuSBgLmKXEoZYDC7V3uzHUCgqp223Mzls",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868040031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_7&ds=v1%3AtM31N3%2FxRPHfPsc3DCq2ZzooaB%2B9CiVOEs4TuSCneRM",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868041031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_8&ds=v1%3Ac5QmH1zBWgXWFNt1%2FwcKK6TlmlRTYG%2FfkAZ0a7SwcH4",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868044031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_9&ds=v1%3ASlx8z5jqO%2FA0hV8qFLIH14yebbOfd0%2BkwRBOoKmB0PI",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868045031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_10&ds=v1%3AR0EthTHfhhh%2Bp0v10zLZo6S5Si3yWTqQp72eWVZbw7g",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868046031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_11&ds=v1%3ASKXPzx4wER%2FLKDt%2F6YonuYE2ZoKsNlDxUzW11UBL7%2FY",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868050031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_12&ds=v1%3AFnKTnDR4vvlMg6uSAN%2BR%2FdzJkmuBYCOcjVG9s%2F0FtwA",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868029031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_13&ds=v1%3Aha9WvnJ9ZNUjEz25OLwg2Nte1vGt5B4Uqdm%2FnIOW5hU",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868053031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_14&ds=v1%3AWL6zJ%2BMjHeZg9WZqnVcp2LNFeRzW9uIlWN3FoAADIUc",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868060031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_15&ds=v1%3AhKvTb2BpZcgZPdKv%2FBjbS125z%2F%2BmCVeKgt0GQUfhDJE",
            "/s?k=namkeen&i=grocery&rh=n%3A2454178031%2Cp_n_feature_browse-bin%3A4868061031&dc&crid=3DD63J3RA42OS&qid=1740130860&rnid=4868020031&sprefix=namkeen%2Caps%2C456&ref=sr_nr_p_n_feature_browse-bin_16&ds=v1%3AULh%2FldUIb%2B0ERxQR9bfqeLiWGoAMXO1%2FuUQAZ1d7Xd8"
        ]
        for speciality_url in speciality_url_list:
            url = "https://www.amazon.in" + speciality_url
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
    cmdline.execute(f"scrapy crawl {AmazonNamkeenSpecialtySpider.name}".split())

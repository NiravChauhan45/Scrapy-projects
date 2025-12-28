import gzip
import hashlib
import json
import os
from datetime import datetime
from typing import Iterable
from googletrans import Translator
import pandas as pd
import scrapy
from scrapy import Request, cmdline
from amf_france.items import AmfFranceItem


class GetdataSpider(scrapy.Spider):
    name = "get_data"
    allowed_domains = ["www.amf-france.org"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_items_native = []
        self.all_items_english = []
        self.current_date = datetime.now().strftime("%d_%m_%Y")

    def start_requests(self):
        url = "https://www.amf-france.org/fr/rest/listing_format/479,40,24,271,480,297/68/all/all/all"
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%228d386952-b9e1-4e66-87c1-b859e54ccd68%22%2C%22options%22%3A%7B%22end%22%3A%222025-11-22T06%3A56%3A13.055Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atauthority=%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22default%22%2C%22visitor_mode%22%3A%22optin%22%7D%2C%22options%22%3A%7B%22end%22%3A%222025-11-22T06%3A56%3A28.261Z%22%2C%22path%22%3A%22%2F%22%7D%7D; tarteaucitron=!facebookpixel=true!atinternetservice=true!fontawesomeservice=true!sondageservice=true!youtube=true; _fbp=fb.1.1729493789766.137709351929575844',
            'priority': 'u=1, i',
            'referer': 'https://www.amf-france.org/fr/espace-epargnants/actualites-mises-en-garde',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        yield scrapy.Request(url=url, headers=headers)

    def parse(self, response, **kwargs):
        json_data = json.loads(response.text)
        data_lst = json_data.get('data')
        for index, data in enumerate(data_lst):
            url = data.get('infos').get('link').get('url')
            theme = data.get('theme')
            title = data.get('infos').get('title')

            page_save_id = int(hashlib.md5(
                bytes(
                    str(url),
                    "utf8")).hexdigest(),
                               16) % (10 ** 18)
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'cookie': 'atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%228d386952-b9e1-4e66-87c1-b859e54ccd68%22%2C%22options%22%3A%7B%22end%22%3A%222025-11-22T06%3A56%3A13.055Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atauthority=%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22default%22%2C%22visitor_mode%22%3A%22optin%22%7D%2C%22options%22%3A%7B%22end%22%3A%222025-11-22T06%3A56%3A28.261Z%22%2C%22path%22%3A%22%2F%22%7D%7D; tarteaucitron=!facebookpixel=true!atinternetservice=true!fontawesomeservice=true!sondageservice=true!youtube=true; _fbp=fb.1.1729493789766.137709351929575844',
                'if-modified-since': 'Mon, 21 Oct 2024 07:58:54 GMT',
                'if-none-match': '"1729497534-gzip"',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.get_data,
                                 meta={'page_save_id': page_save_id, 'theme': theme, 'title': title},
                                 dont_filter=True)

    def get_data(self, response):
        page_save_id = response.meta.get('page_save_id')
        try:
            theme = response.meta.get('theme')
        except Exception as e:
            theme = response.xpath("//ul[@class='list-tags']/li[2]//a//text()").get() if response.xpath(
                "//ul[@class='list-tags']/li[2]//a//text()").get() else 'N/A'

        try:
            date = response.xpath("//div[@class='date']/text()").get() if response.xpath(
                "//div[@class='date']/text()").get() else 'N/A'
        except Exception as e:
            date = 'N/A'

        try:
            title = response.meta.get('title')
        except Exception as e:
            title = response.xpath("//h1[@class='like-h1']/text()").get() if response.xpath(
                "//h1[@class='like-h1']/text()").get() else 'N/A'

        try:
            download_link = response.xpath(
                "//div[contains(@class,'wrapper-download-content')]/a/@href").get()
            if download_link:
                download_link = 'https://www.amf-france.org' + download_link
            else:
                download_link = response.xpath(
                    "//ul[@class='list-simple-link']//a[@class='event-click-atinternet']/@href").get()
        except Exception as e:
            download_link = 'N/A'

        try:
            description = response.xpath("//div[@class='contentToc']/div//text()").get()
            if description:
                description = description
            else:
                description = 'N/A'
        except:
            description = 'N/A'

        try:
            breadcrumb_lst = response.xpath(
                "//div[contains(@class,'breadcrumb')]//font[@style='vertical-align: inherit;']/text()").getall()
            breadcrumb = " | ".join(
                [breadcrumb_data.strip() for breadcrumb_data in breadcrumb_lst]) if breadcrumb_lst else 'N/A'
        except:
            breadcrumb = 'N/A'

        translator = Translator()
        item_native = {
            'theme': theme.strip(),
            'date': date.strip(),
            'title': title.strip(),
            'download_link': download_link.strip(),
            'description': description.strip(),
            'breadcrumb': breadcrumb
        }
        item_english = {
            'theme': str(translator.translate(theme, src='fr', dest='en').text).strip(),
            'date': str(translator.translate(date, src='fr', dest='en').text).strip(),
            'title': str(translator.translate(title, src='fr', dest='en').text).strip(),
            'download_link': str(download_link).strip(),
            'description': str(translator.translate(description, src='fr', dest='en').text).strip(),
            'breadcrumb': breadcrumb
        }

        print(item_native)
        print(item_english)
        print()
        # self.all_items_native.append(item_native)
        # self.all_items_english.append(item_english)
        # with open(f"F:\\Nirav\\Project_page_save\\amf_france\\06_11_2024\\{page_save_id}.html", "w",
        #           encoding="utf-8") as f:
        #     f.write(response.text)
        #     print(f'page save {page_save_id}')

    def close(self, reason):
        # Create a DataFrame and save to Excel when the spider closes
        if self.all_items_native:
            try:
                df = pd.DataFrame(self.all_items_native)
                df.to_excel(
                    f'F:\\Nirav Live Projects\\amf_france\\amf_france\\output_data\\amf_france_native_{self.current_date}.xlsx',
                    index=False)
                self.log(f"Data saved to store_url_old.xlsx because {reason}")
            except Exception as e:
                print(e)
        if self.all_items_english:
            try:
                df = pd.DataFrame(self.all_items_english)
                df.to_excel(
                    f'F:\\Nirav Live Projects\\amf_france\\amf_france\\output_data\\amf_france_english_{self.current_date}.xlsx',
                    index=False)
                self.log(f"Data saved to store_url_old.xlsx because {reason}")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl get_data".split())

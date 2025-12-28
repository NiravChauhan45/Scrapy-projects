import json
import os
import random
from datetime import datetime
from typing import Iterable
import pandas as pd
import requests
import scrapy
from loguru import logger
from scrapy import Request, cmdline, Selector
from doctor_trans import trans


class AllDataSpider(scrapy.Spider):
    name = "all_data"
    allowed_domains = ["www.forbrugerombudsmanden.dk"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_data_items = []
        self.all_data_items_en = []
        self.current_date = datetime.now().strftime("%d_%m_%Y")

    def remove_junk(self, inp_str: str):
        junk_lt = ['\r\n', '\n', '  ', '   ', "'”", " ”'", "\xa0"]
        for junk_ch in junk_lt:
            inp_str = inp_str.replace(junk_ch, '')
        return inp_str

    def start_requests(self):
        pagecount = 0
        while True:
            url = "https://forbrugerombudsmanden.dk/umbraco/api/searchApi/post"
            payload = f'culture=6&currentPageId=79039&include=31528&page={pagecount}&topic=0'
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.7',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://forbrugerombudsmanden.dk',
                'priority': 'u=1, i',
                'referer': 'https://forbrugerombudsmanden.dk/om-os/pressemeddelelser/?page=2',
                'sec-ch-ua': '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            pagecount += 1
            data = json.loads(response.text)
            yield scrapy.Request(url='https://forbrugerombudsmanden.dk',
                                 meta={'data': data}, callback=self.parse, dont_filter=True)
            if len(data.get('Results')) < 10:
                break

    def parse(self, response, **kwargs):
        json_data = response.meta.get('data')
        for data in json_data.get('Results'):
            id = data.get('Id') if data.get('Id') else 'N/A'
            name = data.get('Name') if data.get('Name') else 'N/A'
            teaser = data.get('Teaser') if data.get('Teaser') else 'N/A'
            date = data.get('DateValue') if data.get('DateValue') else 'N/A'
            inhold = data.get('Inhold') if data.get('Inhold') else 'N/A'
            url = "https://forbrugerombudsmanden.dk" + data.get('Url') if data.get('Url') else 'N/A'
            breadcrumbs = " | ".join([i.get('Name') for i in data.get('Breadcrumbs')]) if [i.get('Name') for i in
                                                                                           data.get(
                                                                                               'Breadcrumbs')] else 'N/A'

            # pdp page requests
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'en-US,en;q=0.7',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'referer': 'https://forbrugerombudsmanden.dk/om-os/pressemeddelelser/?page=0',
                'sec-ch-ua': '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'sec-gpc': '1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            }
            yield scrapy.Request(url=url, headers=headers, dont_filter=True, callback=self.pdp_page,
                                 meta={'id': id, 'name': name, 'teaser': teaser, 'date': date, 'inhold': inhold,
                                       'breadcrumbs': breadcrumbs})

    def pdp_page(self, response):
        id = response.meta.get('id')
        name = response.meta.get('name')
        teaser = response.meta.get('teaser')
        date = response.meta.get('date')
        inhold = response.meta.get('inhold')
        breadcrumbs = response.meta.get('breadcrumbs')
        description_lst = response.xpath("//div[@class='Text textContent']//text()").getall()
        description = " ".join(
            [self.remove_junk(inp_str=des) for des in description_lst if self.remove_junk(inp_str=des)])
        item = {
            'Id': id,
            'Name': name,
            'teaser': teaser,
            'date': date,
            'Inhold': inhold,
            'Breadcrumbs': breadcrumbs,
            'Description': description
        }
        self.all_data_items.append(item)

    def close(self, reason):
        if self.all_data_items:
            filepath = "F:\\Nirav\\Project_export_data\\dkforom\\"
            try:
                if not os.path.exists(filepath):
                    os.makedirs(filepath)

                # generating file native language
                main_path = filepath + f"dkforom_native_{self.current_date}.xlsx"
                df = pd.DataFrame(self.all_data_items)

                # generating file in english language
                trans(df, input_lang='auto', output_lang='en',
                      download_file_name=f'F:\\Nirav\\Project_export_data\\dkforom\\dkforom_translated_{self.current_date}.xlsx')
                df.to_excel(main_path, index=False)

                logger.info(f"your file generated.... Total count: {df['Id'].count()}")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl all_data".split())

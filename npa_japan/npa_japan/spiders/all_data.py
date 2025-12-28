from datetime import datetime
from typing import Iterable
from loguru import logger
import pandas as pd
from googletrans import Translator
import scrapy
from scrapy import Request, cmdline


class AllDataSpider(scrapy.Spider):
    name = "all_data"
    allowed_domains = ["www.npa.go.jp"]

    # start_urls = ["https://www.npa.go.jp"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_data_items = []
        self.current_date = datetime.now().strftime("%d_%m_%Y")

    def start_requests(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.6',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        }
        url = "https://www.npa.go.jp/english/bureau/criminal_affairs/wanted_eng.html"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        global crime
        for data in response.xpath("//article[@class='contBlock']//section"):
            # name
            name = data.xpath("./h2/text()").get('').strip() if data.xpath("./h2/text()").get() else 'N/A'

            # image
            image_url = "https://www.npa.go.jp" + data.xpath(".//img/@src").get('').strip() if data.xpath(
                ".//img/@src").get() else 'N/A'

            # Height
            height_data = data.xpath(".//p[contains(text(),'Height')]/text()").get()
            if height_data:
                height = height_data.split('About')[-1].strip()
                if 'Height' in height:
                    height = height_data.split('Height')[-1].strip()
                else:
                    height = height
            else:
                height = 'N/A'

            # Born Year
            born_year_data = data.xpath(".//p[contains(text(),'Born')]/text()").get()
            if born_year_data:
                born_year = born_year_data.split('in')[-1].strip()
            else:
                born_year = 'N/A'

            # crime
            try:
                crime_data = data.xpath(
                    ".//p[contains(text(),'Murder')]/text() | .//p[contains(text(),'Robbery')]/text()").get().strip()
                if crime_data:
                    crime = crime_data
            except:
                crime = 'N/A'

            # phone number
            phone_number = data.xpath(
                ".//p[contains(text(),'Tel')]/text()").get('').strip()
            if phone_number:
                phone_number = phone_number.split('Tel.')[-1].strip().split('(')[0].strip()
            else:
                phone_number = " | ".join([phone_number_data.split('(')[0].strip() for phone_number_data in data.xpath(".//p[contains(text(),'number')]/text()").getall()])

            # address
            address = data.xpath(
                ".//p[contains(text(),'Main phone')]/preceding-sibling::p[position()<2]/text() | .//p[contains(text(),'Toll-free')]/preceding-sibling::p[position()<2]/text() | .//p[contains(text(),'Tel')]/preceding-sibling::p[position()<2]/text()").get(
                '').strip()
            if address:
                address = address
            else:
                address = 'N/A'

            # description
            description = ' '.join(
                data.xpath(".//p[contains(text(),'Height')]/preceding-sibling::p/text()").getall()).strip()
            if description:
                description = description
            else:
                description = 'N/A'

            if name and 'N/A' not in name:
                item = {
                    'Name': name,
                    'Image_url': image_url,
                    'Height': height,
                    'Born_year': born_year,
                    'Crime': crime,
                    'Phone_number': phone_number,
                    'Address': address,
                    'Description': description
                }
                print(item)
                self.all_data_items.append(item)

    def close(self, reason):
        # Create a DataFrame and save to Excel when the spider closes
        if self.all_data_items:
            try:
                df = pd.DataFrame(self.all_data_items)
                df.to_excel(
                    f'F:\\Nirav\\Project_code\\npa_japan\\npa_japan\\output_data\\npa_japan_{self.current_date}.xlsx',
                    index=False)
                logger.info("Your file generated...")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl all_data".split())

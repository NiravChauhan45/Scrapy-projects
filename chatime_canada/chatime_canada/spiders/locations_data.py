import os
import random
from datetime import datetime
from typing import Iterable

from scrapy import Request, cmdline
from chatime_canada.items import ChatimeCanadaStoreLocationItem
from chatime_canada.config.database_config import ConfigDatabase

import scrapy


class LocationsDataSpider(scrapy.Spider):
    name = "locations_data"
    allowed_domains = ["www.chatime.ca"]
    # start_urls = ["https://www.voiply.com"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
    browser = random.choice(["chrome110", "edge99", "safari15_5"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.today_date = datetime.now().strftime("%d_%m_%Y")
        self.page_save_store_location = f'F:\\Nirav\\Project_page_save\\chatime_canada\\page_save_store_location\\{self.today_date}\\'
        self.db = ConfigDatabase(database="chatime_canada", table="find_locations")

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'Pending'})
        for result in results:
            store_no = result['store_no']
            store_name = result['store_name']
            store_url = result['store_url']
            latitude = result['latitude']
            longitude = result['longitude']
            street = result['street']
            zipcode = result['zipcode']
            city_name = result['city_name']
            country_code = result['country_code']
            phone_number = result['phone_number']
            hash_key = result['hash_key']
            access_path = f'{self.page_save_store_location}{str(hash_key)}.html'
            if os.path.exists(access_path):
                yield scrapy.Request(url=f"file:///{access_path}", dont_filter=True,
                                     meta={'store_no': store_no, 'store_name': store_name, 'store_url': store_url,
                                           'latitude': latitude, 'longitude': longitude, 'street': street,
                                           'zipcode': zipcode, 'city_name': city_name, 'country_code': country_code,
                                           'phone_number': phone_number, "hash_key": hash_key,
                                           "impersonate": self.browser})
                # break
            else:
                cookies = {
                    '_fbp': 'fb.1.1728886707471.573253829361901816',
                    '_gid': 'GA1.2.1132395666.1728886708',
                    '_tt_enable_cookie': '1',
                    '_ttp': 'TXFunAIdAC8rJHtNdIZMmaoQ2-3',
                    '_gat_gtag_UA_103247668_1': '1',
                    '_ga_FEFSRLJ26T': 'GS1.1.1728898474.4.1.1728900445.60.0.0',
                    '_ga': 'GA1.1.2062568839.1728886708',
                    '_ga_SBDVRDZ3YG': 'GS1.1.1728898474.4.1.1728900445.0.0.0',
                }
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'max-age=0',
                    # 'cookie': '_fbp=fb.1.1728886707471.573253829361901816; _gid=GA1.2.1132395666.1728886708; _tt_enable_cookie=1; _ttp=TXFunAIdAC8rJHtNdIZMmaoQ2-3; _gat_gtag_UA_103247668_1=1; _ga_FEFSRLJ26T=GS1.1.1728898474.4.1.1728900445.60.0.0; _ga=GA1.1.2062568839.1728886708; _ga_SBDVRDZ3YG=GS1.1.1728898474.4.1.1728900445.0.0.0',
                    # 'if-none-match': '"1053-1728741387;br"',
                    # 'priority': 'u=0, i',
                    # 'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    # 'sec-ch-ua-mobile': '?0',
                    # 'sec-ch-ua-platform': '"Windows"',
                    # 'sec-fetch-dest': 'document',
                    # 'sec-fetch-mode': 'navigate',
                    # 'sec-fetch-site': 'none',
                    # 'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                }
                yield scrapy.Request(url=store_url, cookies=cookies, headers=headers, dont_filter=True,
                                     meta={'store_no': store_no, 'store_name': store_name, 'store_url': store_url,
                                               'latitude': latitude, 'longitude': longitude, 'street': street,
                                               'zipcode': zipcode, 'city_name': city_name, 'country_code': country_code,
                                               'phone_number': phone_number, "hash_key": hash_key,
                                               "impersonate": self.browser})

    def parse(self, response, **kwargs):
        print(response.status)
        try:
            store_no = response.meta.get('store_no')
        except:
            store_no = 'N/A'

        try:
            store_name = response.meta.get('store_name')
        except:
            store_name = 'N/A'

        try:
            store_url = response.meta.get('store_url')
        except:
            store_url = 'N/A'

        try:
            latitude = response.meta.get('latitude')
        except:
            latitude = 'N/A'

        try:
            longitude = response.meta.get('longitude')
        except:
            longitude = 'N/A'

        try:
            street = response.meta.get('street')
        except:
            street = 'N/A'

        try:
            zipcode = response.meta.get('zipcode')
        except:
            zipcode = 'N/A'

        try:
            city_name = response.meta.get('city_name')
        except:
            city_name = 'N/A'

        # country_code = response.meta.get('country_code')
        try:
            phone_number = response.meta.get('phone_number')
        except:
            phone_number = 'N/A'

        page_save_hash_key = response.meta.get('hash_key')

        try:
            Open_hours = " | ".join(
                response.xpath(
                    "//div[@class='store_locator_single_opening_hours']/h2/following-sibling::text()").getall()).replace(
                '  |', ' |')
        except:
            Open_hours = 'N/A'

        try:
            # direction_url = f"https://www.google.com/maps/dir/Current+Location/" + "+".join(
            #     str(street).split(' ')) + ",+".join(city_name.split(' ')) + ',+ON' + ",+".join(
            #     city_name.split(' ')) + ',+Canada/'

            direction_url = f"https://www.google.com/maps/dir/Current+Location/{'+'.join(street.split(' '))},+{'+'.join(city_name.split(' '))},+ON,{'+'.join(zipcode.split(' '))},+Canada/"
        except:
            direction_url = 'N/A'

        item = ChatimeCanadaStoreLocationItem()
        item['Store_No'] = store_no
        item['Name'] = store_name
        item['Latitude'] = latitude
        item['Longitude'] = longitude
        item['Street'] = street
        item['City'] = city_name
        # item['Province'] = ''
        item['Zip_Code'] = zipcode
        item['Phone'] = phone_number
        item['Open_Hours'] = Open_hours
        item['URL'] = store_url
        # item['Provider'] = ''
        item['Updated_date'] = self.today_date
        # item['Country'] = ''
        # item['Status'] = ''
        item['Direction_URL'] = direction_url
        yield item
        # Done/Pending
        try:
            self.db.crsrSql.execute(
                f"update {self.db.table} set status='Done' where hash_key = '{page_save_hash_key}'")
            self.db.connSql.commit()
            print(f"Status for :{page_save_hash_key} Updated=Done")
        except Exception as e:
            print(e)

        # page save
        try:
            if not os.path.exists(self.page_save_store_location):
                os.makedirs(self.page_save_store_location)
            main_path = f'{self.page_save_store_location}{str(page_save_hash_key)}.html'
            if not os.path.exists(main_path):
                with open(main_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"page save for this {page_save_hash_key}")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl locations_data".split())

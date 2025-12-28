import hashlib
import json
import os
import random
from datetime import datetime
from typing import Iterable
# from curl_cffi import requests
import requests
import scrapy
from scrapy import Request, cmdline
from chatime_canada.items import ChatimeCanadaItem


class FindLocationsSpider(scrapy.Spider):
    name = "find_locations"
    today_date = datetime.now().strftime("%d_%m_%Y")
    page_save_store_location = f'F:\\Nirav_page_save\\chatime_canada\\page_save_store_location\\{today_date}\\'

    # allowed_domains = ["https://www.chatime.ca"]
    # start_urls = ["https://www.chatime.ca"]
    def start_requests(self):
        url = "https://chatime.ca/wp-admin/admin-ajax.php"
        payload = "action=get_all_stores&lat=&lng="
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': '_fbp=fb.1.1728886707471.573253829361901816; _gid=GA1.2.1132395666.1728886708; _tt_enable_cookie=1; _ttp=TXFunAIdAC8rJHtNdIZMmaoQ2-3; _ga_FEFSRLJ26T=GS1.1.1728889422.2.1.1728891910.59.0.0; _ga=GA1.1.2062568839.1728886708; _ga_SBDVRDZ3YG=GS1.1.1728889402.2.1.1728892088.0.0.0',
            'origin': 'https://chatime.ca',
            'priority': 'u=1, i',
            'referer': 'https://chatime.ca/locations/?location=905%2C+Canada%2C+Canada&ls_autosearch=1',
            'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        yield scrapy.Request(url='https://google.com', meta={'response_data': response.text})

    def parse(self, response, **kwargs):
        json_data = json.loads(response.meta.get('response_data'))

        for i in range(0, len(json_data) + 1):
            try:
                store_no = json_data.get(str(i)).get('ID')
            except:
                store_no = 'N/A'

            try:
                store_name = json_data.get(str(i)).get('na')
            except:
                store_name = 'N/A'

            try:
                store_url = json_data.get(str(i)).get('gu')
            except:
                store_url = 'N/A'

            try:
                latitude = json_data.get(str(i)).get('lat')
            except:
                latitude = 'N/A'

            try:
                longitude = json_data.get(str(i)).get('lng')
            except:
                longitude = 'N/A'

            try:
                street = json_data.get(str(i)).get('st')
            except:
                street = 'N/A'

            try:
                zipcode = json_data.get(str(i)).get('zp')
            except:
                zipcode = 'N/A'

            try:
                city_name = json_data.get(str(i)).get('ct')
            except:
                city_name = 'N/A'

            try:
                city_code = json_data.get(str(i)).get('co')
            except:
                city_code = 'N/A'

            try:
                phone_number = json_data.get(str(i)).get('te').replace('(', '').replace(') ', '-')
            except:
                phone_number = 'N/A'

            try:
                hash_key = int(hashlib.md5(
                    bytes(
                        str(store_no + store_url + str(latitude) + str(longitude) + str(zipcode) + city_name),
                        "utf8")).hexdigest(),
                               16) % (10 ** 18)
            except:
                hash_key = 'N/A'

            item = ChatimeCanadaItem()
            item['store_no'] = store_no
            item['store_name'] = store_name
            item['store_url'] = store_url
            item['latitude'] = latitude
            item['longitude'] = longitude
            item['street'] = street
            item['zipcode'] = zipcode
            item['city_name'] = city_name
            item['country_code'] = city_code
            item['phone_number'] = phone_number
            item['hash_key'] = hash_key
            yield item

        # page save
        try:
            if not os.path.exists(self.page_save_store_location):
                os.makedirs(self.page_save_store_location)
            main_path = f'{self.page_save_store_location}_all_data.json'
            if not os.path.exists(main_path):
                with open(main_path, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(json_data))
                print(f"page save for this all_data.json")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl find_locations".split())

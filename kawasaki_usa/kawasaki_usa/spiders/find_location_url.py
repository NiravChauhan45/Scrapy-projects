import hashlib
import json
import random
from datetime import datetime
from typing import Iterable

import scrapy
from scrapy import Request, cmdline, Selector

from kawasaki_usa.config.database_config import ConfigDatabase
from kawasaki_usa.items import KawasakiUsaItem


class FindLocationSpider(scrapy.Spider):
    name = "find_location_url"
    allowed_domains = ["www.kawasaki.com"]
    # start_urls = ["https://www.kawasaki.com"]
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
        self.page_save_shop = None
        self.db = ConfigDatabase(database="kawasaki_usa", table="usa_zipcodes")

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'Pending'}) #start=self.start, end=self.end,
        for result in results:
            zip_code = result['zip_code']
            url = f"https://www.kawasaki.com/en-us/PurchaseTools/DealerLocator?LocationFreeText={zip_code}"
            cookies = {
                'CAPIID': 'a45340db-9cb3-42e3-a9e3-a7856e7f4202',
                'usprivacy': '1---',
                'OneTrustWPCCPAGoogleOptOut': 'true',
                'sa-user-id': 's%253A0-5324fb6d-d92a-5aa5-7850-7af775920b92.TQKXmkJFX7PhQmInCQ6S9k%252FtkMUmTqA%252B3vElRUKZRq4',
                'sa-user-id-v2': 's%253AUyT7bdkqWqV4UHr3dZILkpySJFk.PHXRvFYgSVjurO60iQ76XoUsQ4uvhj6JL04NA7wbi1k',
                'sa-user-id-v3': 's%253AAQAKIEFuuQXet_BAaWR8sm-2hHIIllCSQhmimQS6rdseSwL5EAEYAyCwpaK1BjABOgQob8fjQgQdKGhG.UJh65yYp3x5m8x0bYupsbMkgOccH0AzOXHTblig006c',
                '_tt_enable_cookie': '1',
                '_ttp': 'Xh2fFZlF_oAdio8mU9m8dIA-2AE',
                '_ga': 'GA1.1.110178649.1728381733',
                '_fbp': 'fb.1.1728381732707.235998162465875026',
                'prism_1000315808': 'f3119f38-af37-4789-a3f7-b8da2e246163',
                '_gcl_au': '1.1.607332092.1728381733',
                'OptanonAlertBoxClosed': '2024-10-08T10:02:29.305Z',
                'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Oct+08+2024+16%3A30%3A07+GMT%2B0530+(India+Standard+Time)&version=202303.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=3a51ece3-e48b-4e51-9f06-7a1fd528dd72&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CBG72%3A1&geolocation=US%3BNY&AwaitingReconsent=false',
                '_ga_7Y1E113SES': 'GS1.1.1728384622.2.1.1728385225.38.0.0',
            }
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                # 'cookie': 'CAPIID=a45340db-9cb3-42e3-a9e3-a7856e7f4202; usprivacy=1---; OneTrustWPCCPAGoogleOptOut=true; sa-user-id=s%253A0-5324fb6d-d92a-5aa5-7850-7af775920b92.TQKXmkJFX7PhQmInCQ6S9k%252FtkMUmTqA%252B3vElRUKZRq4; sa-user-id-v2=s%253AUyT7bdkqWqV4UHr3dZILkpySJFk.PHXRvFYgSVjurO60iQ76XoUsQ4uvhj6JL04NA7wbi1k; sa-user-id-v3=s%253AAQAKIEFuuQXet_BAaWR8sm-2hHIIllCSQhmimQS6rdseSwL5EAEYAyCwpaK1BjABOgQob8fjQgQdKGhG.UJh65yYp3x5m8x0bYupsbMkgOccH0AzOXHTblig006c; _tt_enable_cookie=1; _ttp=Xh2fFZlF_oAdio8mU9m8dIA-2AE; _ga=GA1.1.110178649.1728381733; _fbp=fb.1.1728381732707.235998162465875026; prism_1000315808=f3119f38-af37-4789-a3f7-b8da2e246163; _gcl_au=1.1.607332092.1728381733; OptanonAlertBoxClosed=2024-10-08T10:02:29.305Z; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+08+2024+16%3A30%3A07+GMT%2B0530+(India+Standard+Time)&version=202303.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=3a51ece3-e48b-4e51-9f06-7a1fd528dd72&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CBG72%3A1&geolocation=US%3BNY&AwaitingReconsent=false; _ga_7Y1E113SES=GS1.1.1728384622.2.1.1728385225.38.0.0',
                'origin': 'https://www.kawasaki.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            # data = {
            #     'LocationFreeText': '34972',
            # }
            yield scrapy.Request(method="POST", url=url, headers=headers, cookies=cookies,
                                 meta={"impersonate": self.browser, 'zip_code': zip_code}, callback=self.parse)

    def parse(self, response, **kwargs):
        zip_code = response.meta.get('zip_code')
        json_data = json.loads(response.text)
        j_data = json_data.get('PartialView')
        selector = Selector(text=j_data)
        dealer_lst = selector.xpath("//li[@class='list-group-item dealer-list pt-3 pb-3']")
        for dealer in dealer_lst:
            store_no = dealer.xpath("./@data-dealernumber").get().strip()
            name = dealer.xpath(".//h2[@class='headFive']/text()").get().strip()
            latitude = dealer.xpath('./@data-dealerlat').get().strip()
            longitude = dealer.xpath('./@data-dealerlng').get().strip()
            street = dealer.xpath('./a/*[2]/text()').get().strip()
            city = dealer.xpath("./a/*[3]/text()").get().split(',')[0].strip()
            state = dealer.xpath("./a/*[3]/text()").get().split(",")[1].strip().split(" ")[0].strip()
            zip_code = dealer.xpath("./a/*[3]/text()").get().split(",")[1].strip().split(" ")[-1].strip()
            phone = dealer.xpath("./a/*[4]/text()").get().strip().replace('(', "").replace(')', '-').strip()
            link = dealer.xpath("//div[@class='generalInfo']/div[@class='listItem contact']/a[@onclick]/@href").get()

            street1 = "+".join(street.split())
            direction = f"https://www.google.com/maps/dir/Current+Location/{street1},+{city},+{state},+{zip_code},+USA/"
            # direction = f"https://www.google.com/maps/dir/Current+Location/{street}{city}{state}{zip_code}USA/"
            updated_date = datetime.now().strftime("%d_%m_%Y")
            hash_key = int(hashlib.md5(
                bytes(
                    str(store_no),
                    "utf8")).hexdigest(),
                           16) % (10 ** 18)

            item = KawasakiUsaItem()
            item['Store_no'] = store_no
            item['Name'] = name
            item['Latitude'] = latitude
            item['Longitude'] = longitude
            item['Street'] = street
            item['City'] = city
            item['State'] = state
            item['Zip_code'] = zip_code
            item['County'] = ''
            item['Phone'] = phone
            item['Url'] = link
            item['Updated_date'] = updated_date
            item['Direction'] = direction
            item['hash_key'] = hash_key
            yield item

            # Done/Pending
            try:
                self.db.crsrSql.execute(
                    f"update {self.db.table} set status='Done' where zip_code = '{zip_code}'")
                self.db.connSql.commit()
                print(f"Status for :{hash_key} Updated=Done")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl find_location_url".split())  # -a start=0 -a end=1000000

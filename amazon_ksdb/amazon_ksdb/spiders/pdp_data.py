from datetime import datetime

import logger
import scrapy
from numpy.lib.utils import source
from scrapy import cmdline
from amazon_ksdb.config.database_config import ConfigDatabase
import amazon_ksdb.config.db_config as db
import amazon_ksdb.spiders.logic_functions as data


class PdpDataSpider(scrapy.Spider):
    name = "pdp_data"
    allowed_domains = ["www.amazon.com"]

    def __init__(self, start_index, end, **kwargs):
        super().__init__(**kwargs)
        self.start_index = start_index
        self.end = end
        self.pagesave = f"E:\\Nirav\\Project_page_save\\amazon_ksdb\\{db.current_date}\\"
        self.db = ConfigDatabase(database=f"{db.database_name}", table=f'{db.input_table}',
                                 start_index=self.start_index,
                                 end=self.end)

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'Pending'}, start_index=self.start_index,
                                              end=self.end)
        for result in results:
            _id = result['id']
            product_id = result['product_id']
            product_url = result['product_url']
            cookies = {
                'session-id': '257-8197099-3389816',
                'i18n-prefs': 'INR',
                'lc-acbin': 'en_IN',
                'ubid-acbin': '261-8449377-2614061',
                'x-amz-captcha-1': '1753007490286758',
                'x-amz-captcha-2': 'sVMDHN3I/qrnn/xSWtXxrA==',
                'session-id-time': '2082787201l',
                'session-token': '+joGIOTHESB8+1IwXuDDgaxMEHcPXsmNH85wiIFSoU85ji3Y2Q7FuZ/J/8JkaNP/EpI6hq1uvSStLesfv5g6JcQfEFtHUYgShDWMnr0qwRUUJxVMD+CqXKZUrOi25gOCkceJt/T441+C+tTyR7aw5F67vIhprYBdjTiFBdHKjdeOzkPgxn9zt1hNsHL0KeUv8A492CwizaLrRuqH3GSdfl2QfVTMKEjGLyuxJNvcv7iEvz7uFPO0lpOGZywNZ+cSRFomjHeOCbQNnsvkML22HNVbmdDzXGK0CUErF9rF3saNuI8hMUhg8txvqgyeI7ElfK8qzrprFM+SP9j1p2Vpw2M2y7goZ21C',
                'csm-hit': 'tb:NFMVJ4TRBT8762KEDE2S+s-R7VDVTD0QH720C9X6E79|1753773278410&t:1753773278410&adb:adblk_no',
                'rxc': 'AKsPUdjTwNDXiy9gBbI',
            }
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'device-memory': '8',
                'downlink': '10',
                'dpr': '1',
                'ect': '4g',
                'priority': 'u=0, i',
                'rtt': '50',
                'sec-ch-device-memory': '8',
                'sec-ch-dpr': '1',
                'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"19.0.0"',
                'sec-ch-viewport-width': '1920',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
                'viewport-width': '1920',
            }
            yield scrapy.Request(url=product_url, cookies=cookies, headers=headers, dont_filter=True,
                                 meta={"product_id": product_id, "product_url": product_url})

    def parse(self, response, **kwargs):

        item = dict()

        # Todo: Input_id, Product_Id, Product_Url
        item['product_url'] = response.meta.get("product_url")
        item['input_pid'] = data.get_product_id(item['product_url'])
        item['product_id'] = data.get_product_id(item['product_url'])
        item['catalog_id'] = data.get_product_id(item['product_url'])

        # Todo: Product Name
        try:
            item['product_name'] = data.get_product_name(response)
            item['catalog_name'] = data.get_product_name(response)
        except:
            item['product_name'] = "N/A"
            item['catalog_name'] = "N/A"

        # Todo: source
        item['source'] = "Amazon"

        # Todo: Scraped_date (YYYY-MM-DD H:M:S)
        try:
            item['scraped_date'] = data.get_scraped_date()
        except Exception as e:
            logger.error(e)

        # Todo: Main Image Url
        try:
            item['Main Image Url'] = data.get_main_image_url(response)
        except:
            item['Main Image Url'] = "N/A"

if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PdpDataSpider.name} -a start_index=1 -a end=1".split())

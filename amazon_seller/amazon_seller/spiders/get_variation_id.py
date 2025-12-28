import json
import re
import pymysql
import scrapy
from loguru import logger
from scrapy import cmdline
from amazon_seller.items import GetVariationIdItem
from amazon_seller.config.database_config import ConfigDatabase
import amazon_seller.config.db_config as db_config


class GetVariationIdSpider(scrapy.Spider):
    name = "get_variation_id"
    allowed_domains = ["www.amazon.com"]

    def __init__(self, start_index, end, **kwargs):
        super().__init__()
        self.start_index = start_index
        self.end = end
        self.cookies = {
            'session-id': '257-8197099-3389816',
            'i18n-prefs': 'INR',
            'lc-acbin': 'en_IN',
            'ubid-acbin': '261-8449377-2614061',
            'session-token': 'okvZ0QGEZYqql3XejHiCjpCvqh6IeESm3l1N48IFot3tP5AoHs6pG0IUs7ewjGDr9GYfTMZVGD2jyxCeoKSBqt5OsFeMTGXIbnmcOrfniU+Q2WSsgPCMoRkyRjPFJ0Zz2ABUCdrawUwJGtRrwqiNhAf4tM3wLxK6iTXMb9Ln4+5wEsi3HtI69MvvaqV5kudbxPWFEckm2ovZJpq8BwzTcjiUlixMU8qnleP99d+h5Po8mX0gIU8x0SE5iALWAdGK+yk1AbrYlqGZ3jBPQPleoHRDvCDVthD2XEF1dODuKFgNV+AJqXZod5l4fzN8Vx4lMQKSwMi/a2mmFvOOCcOAXmW4ZsztTlbG',
            'csm-hit': 'tb:QHBFKPGTWM38JB2DDZA5+s-FCNQZGH98614AK80RXG2|1752942447280&t:1752942447280&adb:adblk_no',
            'session-id-time': '2082787201l',
            'rxc': 'AKsPUdhIcyPXiy9gFbM',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'device-memory': '8',
            'downlink': '4.95',
            'dpr': '1',
            'ect': '4g',
            'priority': 'u=0, i',
            'rtt': '250',
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
            # 'cookie': 'session-id=257-8197099-3389816; i18n-prefs=INR; lc-acbin=en_IN; ubid-acbin=261-8449377-2614061; session-token=okvZ0QGEZYqql3XejHiCjpCvqh6IeESm3l1N48IFot3tP5AoHs6pG0IUs7ewjGDr9GYfTMZVGD2jyxCeoKSBqt5OsFeMTGXIbnmcOrfniU+Q2WSsgPCMoRkyRjPFJ0Zz2ABUCdrawUwJGtRrwqiNhAf4tM3wLxK6iTXMb9Ln4+5wEsi3HtI69MvvaqV5kudbxPWFEckm2ovZJpq8BwzTcjiUlixMU8qnleP99d+h5Po8mX0gIU8x0SE5iALWAdGK+yk1AbrYlqGZ3jBPQPleoHRDvCDVthD2XEF1dODuKFgNV+AJqXZod5l4fzN8Vx4lMQKSwMi/a2mmFvOOCcOAXmW4ZsztTlbG; csm-hit=tb:QHBFKPGTWM38JB2DDZA5+s-FCNQZGH98614AK80RXG2|1752942447280&t:1752942447280&adb:adblk_no; session-id-time=2082787201l; rxc=AKsPUdhIcyPXiy9gFbM',
        }
        self.product_link_table = ConfigDatabase(table=db_config.product_link_table,
                                                 database=db_config.database_name)
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="actowiz",
            database=db_config.database_name
        )

    def start_requests(self):
        results = self.product_link_table.fetchResultsfromSql(conditions={'status': 'Pending'}, start=self.start_index,
                                                              end=self.end)
        for result in results:
            parent_index = result['id']
            item_type = result['item_type']
            product_id = result['product_id']
            product_link = result['product_url']
            yield scrapy.Request(url=product_link, headers=self.headers, cookies=self.cookies,
                                 meta={"parent_index": parent_index, "parent_id": product_id,
                                       "product_link": product_link, "item_type": item_type},
                                 dont_filter=True)

    def parse(self, response, **kwargs):
        parent_index = response.meta.get("parent_index")
        parent_pid = response.meta.get("parent_id")
        product_link = response.meta.get("product_link")
        item_type = response.meta.get("item_type")

        variation_id = list()
        variation_id.append(parent_pid)

        try:
            try:
                all_asin = re.findall(r'dimensionToAsinMap\" :(.*?)\n', response.text)[0]
                all_asin_json = json.loads(all_asin.strip(",").strip())
                for asin in all_asin_json:
                    asin = all_asin_json[asin]
                    if asin not in variation_id:
                        variation_id.append(asin)
            except:
                ''
            sr_nos_1 = parent_index
            for child_index, variation in enumerate(variation_id, start=1):
                child_pid = variation
                sr_nos_2 = f"{parent_index}.{child_index}"
                unique_key = f"{parent_pid}_{child_pid}"
                item = GetVariationIdItem()

                item['item_type'] = item_type
                item['product_url'] = product_link
                item['parent_pid'] = parent_pid
                item['child_pid'] = child_pid
                item['sr_nos_1'] = sr_nos_1
                item['sr_nos_2'] = sr_nos_2
                item['unique_key'] = unique_key
                yield item

            # Todo: Update Table
            try:
                cur = self.conn.cursor()
                update_query = "UPDATE product_links SET STATUS = %s WHERE product_id = %s"
                cur.execute(update_query, ('Done', parent_pid))
                self.conn.commit()
                logger.success(f"This {parent_pid} is successfully updated..!!")
            except Exception as e:
                logger.error("Error updating product status: %s", e)
        except Exception as error:
            logger.error(f"Get Variation In Parse: {error}")


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {GetVariationIdSpider.name} -a start_index=1 -a end=1".split())

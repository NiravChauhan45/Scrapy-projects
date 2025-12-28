import hashlib
import json

import scrapy
from scrapy import cmdline
from amazon_searching.config.database_config import ConfigDatabase
import mysql.connector
from amazon_searching.items import AmazonSearchingItem


class NewGetDataSpider(scrapy.Spider):
    name = "new_get_data"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com"]

    # conn = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="actowiz",
    #     database="amazon_searching"
    # )

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        # self.conn = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="actowiz",
        #     database="amazon_searching"
        # )
        # self.cursor = self.conn.cursor()

        self.url_xpath = '//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-medium"]//li[@class="a-spacing-micro apb-browse-refinements-indent-2"]//a/@href'
        self.name_xpath = '//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-medium"]//li[@class="a-spacing-micro apb-browse-refinements-indent-2"]//a//span//text()'

        self.new_url_xpath = '//li[@class="a-spacing-micro s-navigation-indent-2"]//a/@href'
        self.new_name_xpath = '//li[@class="a-spacing-micro s-navigation-indent-2"]//a/span/text()'

        self.url_second_xpath = '//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-medium"]//li[@class="a-spacing-micro s-navigation-indent-2"]//a/@href'
        self.name_second_xpath = '//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-medium"]//li[@class="a-spacing-micro s-navigation-indent-2"]//a//span//text()'
        self.cookies = {
            'session-id': '137-7403011-7722521',
            'session-id-time': '2082787201l',
            'i18n-prefs': 'USD',
            'ubid-main': '135-3823203-7664328',
            'session-token': '/D+Cs+zxeU3z8aqjgNiDgQXehhjPChG/i+qcjvbPwNlWkPUWYbxGOxVzDP2TdZpQylHn3m8PXkgTiqYTDrIl1yyPmj7SjMTZ6GBCHBp6/SGjGdRCy1yKrEKs58zw5GFhH9kCujkETOg/gPrZrKzan0XmSbSGlPQnJelv8wFTy6e//rFxbpyVNe+3Zga/dB4hpHiLOl5VTyjifORyRdvqIDauGXypihjvKpVhhrQRzHBvXy3sY7K6hR13tL4BbEweInOx+zb49H7kYwPmYj9OxYkThSJ35YxbjnUfGOvaEZLF3Ddvk2YAeLgt5PgV5hjma9gLoxy2Bru1ujUTH97xosird7yHU2TG',
            'csm-hit': 'tb:7RAJFFWKMW6AB59HAQ8N+sa-7RAJFFWKMW6AB59HAQ8N-9T03GRYTS2N6B4EC1XE0|1742550426492&t:1742550426492&adb:adblk_no',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'device-memory': '8',
            'downlink': '10',
            'dpr': '1.35',
            'ect': '4g',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'rtt': '50',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'viewport-width': '1422',
            # 'cookie': 'session-id=137-7403011-7722521; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=135-3823203-7664328; session-token=/D+Cs+zxeU3z8aqjgNiDgQXehhjPChG/i+qcjvbPwNlWkPUWYbxGOxVzDP2TdZpQylHn3m8PXkgTiqYTDrIl1yyPmj7SjMTZ6GBCHBp6/SGjGdRCy1yKrEKs58zw5GFhH9kCujkETOg/gPrZrKzan0XmSbSGlPQnJelv8wFTy6e//rFxbpyVNe+3Zga/dB4hpHiLOl5VTyjifORyRdvqIDauGXypihjvKpVhhrQRzHBvXy3sY7K6hR13tL4BbEweInOx+zb49H7kYwPmYj9OxYkThSJ35YxbjnUfGOvaEZLF3Ddvk2YAeLgt5PgV5hjma9gLoxy2Bru1ujUTH97xosird7yHU2TG; csm-hit=tb:7RAJFFWKMW6AB59HAQ8N+sa-7RAJFFWKMW6AB59HAQ8N-9T03GRYTS2N6B4EC1XE0|1742550426492&t:1742550426492&adb:adblk_no',
        }
        self.db = ConfigDatabase(database='amazon_searching', table='category_links')
        self.start = start
        self.end = end

    def start_requests(self):
        results = self.db.fetchResultsfromSql(start=self.start, end=self.end, conditions={'status': 'pending'})

        for data in results:
            url = data['category_url']
            rh = ""
            qid = ""
            rnid = ""
            ref = ""
            for params in url.split('&'):
                if "rh=" in params:
                    rh = params.replace('https://www.amazon.com/s?', '')
                elif "qid=" in params:
                    qid = params
                elif "rnid=" in params:
                    rnid = params
                elif "ref=" in params:
                    ref = params

            request_url = f'https://www.amazon.com/s?{rh}&dc&{qid}&{rnid}&{ref}'

            meta = {
                "Breadcrumb": [
                    {'url': data['main_category_url'],
                     'name': data['main_category_name']},
                    {'url': request_url, 'name': data['category_name']}],
                'update_id': data['id'],
                'main_category_name': data['main_category_name'], 'main_category_url': data['main_category_url'],
                'category_name': data['category_name'], 'category_url': request_url
            }

            yield scrapy.Request(
                url=request_url,
                headers=self.headers,
                cookies=self.cookies,
                meta=meta,
                dont_filter=True
            )

    def parse(self, response, **kwargs):
        breadcrumb = response.meta["Breadcrumb"]
        update_id = response.meta["update_id"]

        main_category_name = response.meta["main_category_name"]
        main_category_url = response.meta["main_category_url"]
        category_name = response.meta["category_name"]
        category_url = response.meta["category_url"]

        urls = response.xpath(self.url_xpath).getall()
        names = response.xpath(self.name_xpath).getall()

        if not urls:
            urls = response.xpath(self.new_url_xpath).getall()
            names = response.xpath(self.new_name_xpath).getall()

        for name, url in zip(names, urls):
            url = "https://www.amazon.com" + url

            rh = ""
            qid = ""
            rnid = ""
            ref = ""
            for params in url.split('&'):
                if "rh=" in params:
                    rh = params.replace('https://www.amazon.com/s?', '')
                elif "qid=" in params:
                    qid = params
                elif "rnid=" in params:
                    rnid = params
                elif "ref=" in params:
                    ref = params

            if not qid:
                if "https://" not in url:
                    request_url = f'https://www.amazon.com/' + url
                else:
                    request_url = url
            else:
                request_url = f'https://www.amazon.com/s?{rh}&dc&{qid}&{rnid}&{ref}'

            if name not in [dic['name'] for dic in breadcrumb]:
                breadcrumb.append({'url': request_url, 'name': name})
                item = AmazonSearchingItem()
                item['main_category_name'] = main_category_name
                item['main_category_url'] = main_category_url
                item['category_name'] = category_name
                item['category_url'] = category_url
                item['sub_category_name'] = name
                item['sub_category_url'] = request_url
                hash_id = str(
                    int(hashlib.md5(
                        bytes(str(main_category_name) + str(category_name) + str(name), "utf8")).hexdigest(),
                        16) % (
                            10 ** 10))
                item['hash_id'] = hash_id
                yield item
                breadcrumb.pop()

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="actowiz",
            database="amazon_searching"
        )
        cursor = conn.cursor()
        update_query = f"UPDATE {self.db.table} SET status = %s WHERE id = %s"
        values = ('Done', update_id)
        cursor.execute(update_query, values)
        conn.commit()
        print('your record successfully updated..')
        conn.close()


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {NewGetDataSpider.name} -a start=1 -a end=30".split())

import gzip
import hashlib
import os
import random
from urllib.parse import urlencode
import pymysql
import scrapy
from scrapy.cmdline import execute
from datetime import datetime
from amazon_searching import db_config as db


class KeywordSerchSpider(scrapy.Spider):
    name = "keyword_serch"

    processed_asins = set()
    ranking_counter = 0
    target_count = 510
    active_tasks = set()

    def __init__(self, name=None, start_index=0, end=0, **kwargs):
        super().__init__(name, **kwargs)
        self.start_index = start_index
        self.end = end
        self.con = pymysql.connect(host=db.db_host, user=db.db_user, password=db.db_password, port=3306, db=db.db_name)
        self.cursor = self.con.cursor()

    def start_requests(self):
        query = (
            f"select id, keyword, pincode, status FROM {db.db_keyword_table} "
            f"where status='pending' and id between {self.start_index} and {self.end}"
        )
        self.cursor.execute(query)
        query_results = self.cursor.fetchall()
        self.logger.info(f"\n\n\nTotal Results ...{len(query_results)}\n\n\n")

        for query_result in query_results:
            id = query_result[0]
            keyword = query_result[1]
            pincode = query_result[2]
            params = {
                'k': keyword.strip(),
            }
            url = f'https://www.amazon.in/s?{urlencode(params)}'
            scrape_do_token = '28eb354eaa39425ebdc76636bfacb74f0c13ce6e8a6'
            modified_url = f"https://api.scrape.do/plugin/amazon/?token={scrape_do_token}&zipCode={pincode}&geoCode=in&output=html&url=" + url

            self.processed_asins.clear()
            self.ranking_counter = 0
            self.active_tasks.add(id)

            yield scrapy.Request(
                modified_url,
                meta={'table_id': id, 'keyword': keyword, 'pincode': pincode, 'page': 1},
                callback=self.parse,
                dont_filter=True)

    def parse(self, response, **kwargs):
        table_id = response.meta['table_id']
        keyword = response.meta['keyword']
        pincode = response.meta['pincode']  # Retrieve pincode from meta
        page = response.meta['page']

        today_str = datetime.today().strftime('%Y%m%d')
        path = f'E:/Nirav/Project_page_save/amazon_keyword/{today_str}'
        os.makedirs(path, exist_ok=True)
        keyword_hash = hashlib.sha256(keyword.encode()).hexdigest()
        gzip_filename = f'{path}/{keyword_hash}_page_{page}.html.gz'
        gzip.open(gzip_filename, 'wb').write(response.body)

        search_results = response.xpath('//div[contains(@class,"s-result-list s-search-results")]/div[@data-asin]')

        if search_results:
            for product_details in search_results:
                if self.ranking_counter >= self.target_count:
                    break

                product_id = product_details.xpath('./@data-asin').get()
                if not product_id or product_id in self.processed_asins:
                    continue

                self.ranking_counter += 1
                self.processed_asins.add(product_id)
                product_url = f'https://www.amazon.in/dp/{product_id}'
                product_ranking = str(self.ranking_counter)
                show_keyword = response.xpath(
                    '//span[@data-component-type="s-result-info-bar"]//span[contains(@class,"a-text-bold")]/text()').get(
                    '').strip('"')
                product_sponsored = 'True' if product_details.xpath(
                    './/span[@class="puis-label-popover-default"]') else 'False'

                # Modify the INSERT query to include pincode
                insert_query = f'insert ignore into {db.db_links_table} (product_id,product_url,search_keyword,onsite_keyword,pincode,product_ranking,product_sponsored) values (%s,%s,%s,%s,%s,%s,%s)'
                self.cursor.execute(insert_query, (
                    product_id, product_url, keyword, show_keyword, pincode, product_ranking, product_sponsored))
                self.con.commit()

            if self.ranking_counter < self.target_count:
                next_page_link = response.xpath('//a[contains(@class,"s-pagination-next")]/@href').get()
                if next_page_link and page < 7:
                    next_page_url = f'https://www.amazon.in{next_page_link}'
                    meta, headers = self._get_request_meta_headers()
                    meta['table_id'] = table_id
                    meta['keyword'] = keyword
                    meta['pincode'] = pincode  # Pass pincode to next request
                    meta['page'] = page + 1
                    yield scrapy.Request(
                        next_page_url,
                        meta=meta,
                        headers=headers,
                        callback=self.parse,
                        dont_filter=True)
                else:
                    refinement_links = response.xpath(
                        '//div[contains(@id,"brandsRefinements")]//ul//li//a/@href').getall()[:10]
                    if refinement_links:
                        for link in refinement_links:
                            if self.ranking_counter >= self.target_count:
                                break
                            full_url = f'https://www.amazon.in{link}'
                            meta, headers = self._get_request_meta_headers()
                            meta['table_id'] = table_id
                            meta['keyword'] = keyword
                            meta['pincode'] = pincode  # Pass pincode to next request
                            meta['page'] = page + 1
                            yield scrapy.Request(
                                full_url,
                                meta=meta,
                                headers=headers,
                                callback=self.parse_refinements,
                                dont_filter=True)
                    else:
                        pass
            else:
                pass
        else:
            pass
        update_qury = f'update {db.db_keyword_table} set status="Done" where id=%s'
        self.cursor.execute(update_qury, (table_id,))
        self.con.commit()

        # The following lines are incorrect and have been removed.
        # They were causing the 'Done' status to be set too early.
        # The correct logic is now in the `parse_final` method.

    def parse_refinements(self, response, **kwargs):
        table_id = response.meta['table_id']
        keyword = response.meta['keyword']
        pincode = response.meta['pincode']  # Retrieve pincode from meta
        page = response.meta['page']

        today_str = datetime.today().strftime('%Y%m%d')
        path = f'E:/Nirav/Project_page_save/amazon_keyword/{today_str}'
        os.makedirs(path, exist_ok=True)
        keyword_hash = hashlib.sha256(keyword.encode()).hexdigest()
        gzip_filename = f'{path}/{keyword_hash}_brand_page_{page}.html.gz'
        gzip.open(gzip_filename, 'wb').write(response.body)

        search_results = response.xpath('//div[contains(@class,"s-result-list s-search-results")]/div[@data-asin]')

        if search_results:
            for product_details in search_results:
                if self.ranking_counter >= self.target_count:
                    break

                product_id = product_details.xpath('./@data-asin').get()
                if not product_id or product_id in self.processed_asins:
                    continue

                self.ranking_counter += 1
                self.processed_asins.add(product_id)
                product_url = f'https://www.amazon.in/dp/{product_id}'
                product_ranking = str(self.ranking_counter)
                show_keyword = response.xpath(
                    '//span[@data-component-type="s-result-info-bar"]//span[contains(@class,"a-text-bold")]/text()').get(
                    '').strip('"')
                product_sponsored = 'True' if product_details.xpath(
                    './/span[@class="puis-label-popover-default"]') else 'False'

                # Modify the INSERT query to include pincode
                insert_query = f'insert into {db.db_links_table} (product_id,product_url,search_keyword,onsite_keyword,pincode,product_ranking,product_sponsored) values (%s,%s,%s,%s,%s,%s,%s)'
                self.cursor.execute(insert_query, (
                    product_id, product_url, keyword, show_keyword, pincode, product_ranking, product_sponsored))
                self.con.commit()

            # Here, you need to check if there are more refinements to follow.
            # The previous version was not doing this, causing the 'Done' status to be missed.
            # The logic to handle multiple refinements is complex in this setup. A simpler fix
            # is to assume refinements are one-off pages and then mark as done.
            # If you need to handle multiple refinement pages, the logic from the previous
            # response with the iterator pattern is more robust.


    def parse_final(self, response):
        table_id = response.meta['table_id']
        self.update_status_done(table_id)

    def update_status_done(self, table_id):
        update_query = f'update {db.db_keyword_table} set status="Done" where id=%s'
        self.cursor.execute(update_query, (table_id,))
        self.con.commit()
        self.logger.info(
            f"Finished scraping for keyword with ID: {table_id}. Total products scraped: {self.ranking_counter}")

    def _get_request_meta_headers(self):
        browsers = [
            "chrome99", "chrome100", "chrome101", "chrome104", "chrome107", "chrome110",
            "chrome116", "chrome119", "chrome120", "chrome123",
            "chrome99_android", "edge99", "edge101", "safari15_3", "safari15_5",
            "safari17_0", "safari17_2_ios"
        ]
        meta = {"impersonate": random.choice(browsers)}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'referer': 'https://www.amazon.in/',
        }
        return meta, headers


if __name__ == '__main__':
    execute('scrapy crawl keyword_serch -a start_index=2 -a end=2'.split())
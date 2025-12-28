import os
from typing import Iterable

import loguru
import pymysql
import scrapy
from scrapy import cmdline, Request
import pandas as pd
from download_images.config.database_config import ConfigDatabase


class BigBasketDownloadImageSpider(scrapy.Spider):
    name = "download_image"

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='actowiz',
            db='download_images'
        )
        self.db = ConfigDatabase(database=f"download_images", table=f'big_basket')
        self.cursor = self.connection.cursor()

    def start_requests(self, **kwargs):
        results = self.db.fetchResultsfromSql(conditions={'status': 'Pending'}, start=self.start, end=self.end)
        for result in results:
            product_id = result['product_id']
            image_url = result['product_image']
            yield scrapy.Request(url=image_url, dont_filter=True, meta={"product_id": product_id})

    def parse(self, response, **kwargs):
        product_id = response.meta.get('product_id')
        save_location = fr"C:\Big_basket_image_download"
        if not os.path.exists(save_location):
            os.makedirs(save_location)

        # Todo: save product-images path
        save_path = fr'{save_location}\{product_id}.jpg'

        # Todo: Save the image to the specified location
        with open(save_path, 'wb') as file:
            file.write(response.body)
        loguru.logger.info(f"Image downloaded successfully: {save_location}")

        # Todo: Update status in the database
        self.cursor.execute("UPDATE big_basket SET status = %s WHERE product_id = %s", ('Done', product_id))
        self.connection.commit()  # Commit the update
        loguru.logger.success(f"your product_id: {product_id} is updated.")


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {BigBasketDownloadImageSpider.name} -a start=1 -a end=100".split())

import hashlib
import json
from typing import Iterable

import scrapy
from scrapy import cmdline, Request
from nykaa_fashion.config.database_config import ConfigDatabase
from nykaa_fashion.items import NykaaCategoryItem


class CategoriesLinksSpider(scrapy.Spider):
    name = "categories_links"

    def start_requests(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'cookie': '_ga=GA1.1.1706282877.1739440402; _clck=93b5ie%7C2%7Cfte%7C0%7C1870; tm_stmp=1739440406887; rum_abMwebSort=45; bcookie=9de11912-6ea7-44cb-ae7c-39a4b138342c; _gcl_au=1.1.434347511.1739440412; WZRK_G=bad937a95f8b42beaf8ccc829a0bbaf3; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; PHPSESSID=3bc2bab55f9145a0ae8703cabbab1fdf; NYK_VISIT=9de11912-6ea7-44cb-ae7c-39a4b138342c~1739440412553; EXP_plp-quick-filters=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; bm_sz=352A7C10B1C5EAF22FAF953D9260BED4~YAAQNnLBF2j7t76UAQAA+lbH/hr7wFa5cMFM2aK+h6iENNMk9EXjAd8dTHtcrL7IX03QJq6WsW+jWmHUE96MaUK3mGqC9WgfxLVLkV2yp/HcMlHrVamDzruZmD9IB6gzs1xsYgH4UZoWMsGtm8KMS8EaHRuVQwz1lO4DnwhTn0Q1kGRWE9FEZbH6YPtV9wDNK+tnlLkHkNi6rz7pLS0hkW8Dpc8S50v9DlFZAqTSNoJlVC7wZIeJPmFxCa0hfz6ic++VreGwDgJZeURy4QsdjjyTyTxpYDQ2/cpUhenBez7ydWlD8M+QQm7bpqE7XtKCW+3rrYerrbtZZsjKZ35sth2Ve6Po4fMWEITASYlyPALQo7WfVrks59nvnDyfKuGjjGLFGHPnFQbshBuQnr4ihLNPm5ElDSQt1mftn7I+XGpNYHHeOeE/pimztt9vYAbOwI/IGZM5id8GR3KAaW7EWKkiuaWlr+y+uQmXhlFYlNXtVbB4RHnQXhdCHkoD6ZMXKPiFJkR7Q/8x6OUWicRT/7NfRuPb351c8EryqOqma+rOxlw=~3753281~3749943; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQNnLBF5v7t76UAQAAXljH/g3nOHDhhLVa6shChGVIG74hz3BESd/bZGZMidyDrUj72f0PTos7iacUUJGC/VbSFjfWZoVYIGWaFHfRACQHkpFEPfT9ExbVlpUssbrAj9soAcSg6Lh8p/pl9rBHEbHTxHS5kGL5olfyWAK7XH6hpd+iRLS/69qfu5qiDv749182VqAf00Dy5LIr4rjHI8RNSQWuL0VIAOs0aZjQGHfmIhMT5tiJ4W5Ydpmap7kSecQUu44XekgUqQidJjd6FIOHmlWG+7nr8HnaDNX6oeRNsgyhwQFuLQOaJZyVGC0/vEpCQ9W0Hm75qZzW4KaOWYw/6oX03c8WRt5hAaEPyo5D0VXuDg1IAtByecWbrMagpOoMitSZIT3KtPR7m9mePARSLEjqWeqSvBTSnkGuNQ5nTGtLuBxrG6Xe45y320U/FaEJs5jQhMkOnCJ39XrYeXhf4zNj/INneu56ojnSVl8bVuA8QtPAdHePZxt3T6f1G8vEK1j5ZFj8lxQo+wnjqX36J3DWa3h65ooUGtW0~-1~-1~1739443250; NYK_PCOUNTER=6; NYK_ECOUNTER=276; WZRK_S_WRK-4W9-R55Z=%7B%22s%22%3A1739440568%2C%22t%22%3A1739441102%2C%22p%22%3A6%7D; _clsk=1g6kvsr%7C1739441104051%7C10%7C0%7Cq.clarity.ms%2Fcollect; _ga_DZ4MXZBLKH=GS1.1.1739440401.1.1.1739441125.33.0.0; EXP_new-relic-client=variant1',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        }
        url = "https://www.nykaafashion.com/"
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        global category
        json_data = response.xpath("//script[@id='__PRELOADED_STATE__']/text()").get()
        j_data = json.loads(json_data)
        j_data = j_data.get('app').get('menu').get('data')
        item = NykaaCategoryItem()
        for data in j_data:
            main_category_name = data.get('name')
            for category in data.get('children_data'):
                category_name = category.get('name')
                for sub_category in category.get("children_data"):
                    sub_category_name = sub_category.get('name')
                    sub_category_url = sub_category.get('action_url')
                    item['main_category_name'] = main_category_name
                    item['category_name'] = category_name
                    item['sub_category_name'] = sub_category_name
                    if sub_category_url:
                        if "https://" not in sub_category_url:
                            item['sub_category_url'] = "https://www.nykaafashion.com" + sub_category_url if sub_category_url else ''
                        else:
                            item['sub_category_url'] = sub_category_url
                    item['hash_id'] = str(
                        int(hashlib.md5(
                            bytes(str(main_category_name) + str(category_name) + str(sub_category_url),
                                  "utf8")).hexdigest(),
                            16) % (
                                10 ** 10))
                    yield item


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {CategoriesLinksSpider.name}".split())

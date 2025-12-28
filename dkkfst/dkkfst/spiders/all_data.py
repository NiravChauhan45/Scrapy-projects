from datetime import datetime
from typing import Iterable

import pandas as pd
import scrapy
from loguru import logger
from parsel import Selector
from scrapy import cmdline, Request
import re


class AllDataSpider(scrapy.Spider):
    name = "all_data"
    allowed_domains = ["www.en.kfst.dk"]

    def remove_punctuation(self, text):
        text = text.replace('\xa0', ' ')
        return re.sub(r'[^\w\s&/]', '', text)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_data_items = []
        self.current_date = datetime.now().strftime("%d_%m_%Y")

    def start_requests(self):
        url = 'https://en.kfst.dk/competition/about-competition-matters/penalties-for-infringing-the-danish-competition-act/fines-in-competition-cases/'
        cookies = {
            'CookieInformationConsent': '%7B%22website_uuid%22%3A%22df0c86fe-e9b2-461a-8a1b-6f0c4687e027%22%2C%22timestamp%22%3A%222024-11-11T05%3A48%3A41.612Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fen.kfst.dk%2Fcompetition%2Fabout-competition-matters%2Fpenalties-for-infringing-the-danish-competition-act%2Ffines-in-competition-cases%2F%22%2C%22consent_website%22%3A%22en.kfst.dk%2F%22%2C%22consent_domain%22%3A%22en.kfst.dk%22%2C%22user_uid%22%3A%2257427ec7-db55-47d5-b21c-cac848e3b395%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%5D%2C%22consents_denied%22%3A%5B%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F130.0.0.0%20Safari%2F537.36%22%7D',
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': 'CookieInformationConsent=%7B%22website_uuid%22%3A%22df0c86fe-e9b2-461a-8a1b-6f0c4687e027%22%2C%22timestamp%22%3A%222024-11-11T05%3A48%3A41.612Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fen.kfst.dk%2Fcompetition%2Fabout-competition-matters%2Fpenalties-for-infringing-the-danish-competition-act%2Ffines-in-competition-cases%2F%22%2C%22consent_website%22%3A%22en.kfst.dk%2F%22%2C%22consent_domain%22%3A%22en.kfst.dk%22%2C%22user_uid%22%3A%2257427ec7-db55-47d5-b21c-cac848e3b395%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%5D%2C%22consents_denied%22%3A%5B%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F130.0.0.0%20Safari%2F537.36%22%7D',
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
        yield scrapy.Request(url=url, cookies=cookies, headers=headers, dont_filter=True)

    def parse(self, response, **kwargs):
        data = response.xpath("//div[contains(@class,'Grid-cell u-size6')]//script[1]/text()").get()
        html_data = data.split(" ")[-1].split('.replace(/&lt;/g, "<")')[0].replace( "&lt;", "<").replace(
            "&gt;", ">").replace("&quot;", "\"").replace("&#39;", "\'").replace("&amp;", "&")

        selector = Selector(text=html_data)

        response_data_lst = selector.xpath("//table[@class='standard-table']//tr")

        for response_data in response_data_lst:
            try:
                year = response_data.xpath('.//td[1]//text()').get().strip()
            except:
                year = 'N/A'

            try:
                company_data = " ".join([i.strip() for i in response_data.xpath(".//td[2]//text()").getall()])
                company = self.remove_punctuation(company_data)
            except:
                company = 'N/A'

            try:
                fine_and_DKK = " ".join(response_data.xpath(".//td[3]//text()").getall()).replace('  ',' ').replace('\xa0','')
            except:
                fine_and_DKK = 'N/A'

            try:
                infringement = " ".join([i for i in response_data.xpath("./td[4]//text()").getall()]).strip().replace(
                    '  ', ' ') if " ".join(
                    [i for i in response_data.xpath("./td[4]//text()").getall()]).strip() else 'N/A'
            except:
                infringement = 'N/A'

            try:
                conviction_and_settlement = " ".join(
                    [i.strip() for i in response_data.xpath(".//td[5]//text()").getall()]).strip()
            except:
                conviction_and_settlement = 'N/A'

            item = {
                'Year': year,
                'Company': company,
                'Fine and DKK': fine_and_DKK,
                'Infringement': infringement,
                'Conviction/Settlement': conviction_and_settlement
            }
            self.all_data_items.append(item)

    def close(self, reason):
        # Create a DataFrame and save to Excel when the spider closes
        if self.all_data_items:
            try:
                df = pd.DataFrame(self.all_data_items)
                df[1:].to_excel(
                    f'F:\\Nirav\\Project_code\\dkkfst\\dkkfst\\output_data\\dkkfst_{self.current_date}.xlsx',
                    index=False)
                logger.info("Your file generated...")
            except Exception as e:
                print(e)


#
if __name__ == '__main__':
    cmdline.execute("scrapy crawl all_data".split())
